import logging

from apps.cases import populate
from apps.cases.models import (
    Address,
    Case,
    CaseTimelineReaction,
    CaseTimelineSubject,
    CaseTimelineThread,
    CaseType,
    State,
    StateType,
)
from apps.cases.serializers import (
    AddressSerializer,
    CaseSerializer,
    CaseThreadCreationSerializer,
    CaseThreadUpdateSerializer,
    CaseTimelineReactionSerializer,
    CaseTimelineSerializer,
    CaseTimelineSubjectSerializer,
    CaseTimelineThreadSerializer,
    CaseTypeSerializer,
    FineListSerializer,
    ResidentsSerializer,
    StateSerializer,
    StateTypeSerializer,
)
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from utils.api_queries_belastingen import get_fines, get_mock_fines
from utils.api_queries_brp import get_brp
from utils.api_queries_decos_join import (
    get_decos_join_permit,
    get_decos_join_request,
    get_decos_join_request_swagger,
)

logger = logging.getLogger(__name__)


class GenerateMockViewset(ViewSet):
    def list(self, request):
        populate.delete_all()
        case_types = populate.create_case_types()
        state_types = populate.create_state_types()
        addresses = populate.create_addresses()
        cases = populate.create_cases(case_types, addresses)
        states = populate.create_states(cases, state_types)

        return Response(
            {
                "case_types": CaseTypeSerializer(case_types, many=True).data,
                "addresses": AddressSerializer(addresses, many=True).data,
                "cases": CaseSerializer(cases, many=True).data,
                "state_types": StateTypeSerializer(state_types, many=True).data,
                "states": StateSerializer(states, many=True).data,
            }
        )


class CaseViewSet(ViewSet, ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CaseSerializer
    queryset = Case.objects.all()
    lookup_field = "identification"

    @action(detail=True, methods=["get"], serializer_class=ResidentsSerializer)
    def residents(self, request, identification):
        try:
            case = Case.objects.get(identification=identification)
        except Case.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            bag_id = case.address.bag_id
            brp_data = get_brp(bag_id)
            serialized_residents = ResidentsSerializer(data=brp_data)
            serialized_residents.is_valid()

            return Response(serialized_residents.data)

        except Exception as e:
            logger.error(f"Could not retrieve residents for case {identification}: {e}")

            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"], serializer_class=FineListSerializer)
    def fines(self, request, identification):
        """Retrieves states for a case which allow fines, and retrieve the corresponding fines"""
        states = Case.objects.get(identification=identification).states
        eligible_states = states.filter(state_type__invoice_available=True).all()
        states_with_fines = []

        for state in eligible_states:
            try:
                fines = get_fines(state.invoice_identification)
                serialized_fines = FineListSerializer(data=fines)
                serialized_fines.is_valid()
                serialized_state = StateSerializer(state)

                response_dict = {
                    **serialized_state.data,
                    "fines": serialized_fines.data.get("items"),
                }
                states_with_fines.append(response_dict)
            except Exception as e:
                logger.error(
                    f"Could not retrieve fines for {state.invoice_identification}: {e}"
                )

        # TODO: Remove 'items' (because it's mock data) from response once we have an anonimizer
        fines = get_mock_fines("foo_id")
        data = {"items": fines["items"], "states_with_fines": states_with_fines}

        serialized_fines = FineListSerializer(data=data)
        serialized_fines.is_valid()

        return Response(serialized_fines.data)


class AddressViewSet(ViewSet, ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class CaseTypeViewSet(ViewSet, ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CaseTypeSerializer
    queryset = CaseType.objects.all()


class StateTypeViewSet(ViewSet, ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StateTypeSerializer
    queryset = StateType.objects.all()


class StateViewSet(ViewSet, ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StateSerializer
    queryset = State.objects.all()


query = OpenApiParameter(
    name="query",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=True,
    description="Query",
)

book_id = OpenApiParameter(
    name="book_id",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=True,
    description=(
        "BAG Objecten: 90642DCCC2DB46469657C3D0DF0B1ED7 or Objecten onbekend:"
        " B1FF791EA9FA44698D5ABBB1963B94EC"
    ),
)

object_id = OpenApiParameter(
    name="object_id",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=True,
    description="ID van woningobject",
)

permit_search_parameters = [book_id, query]
permit_request_parameters = [query]


class PermitViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=permit_search_parameters, description="Search query parameters"
    )
    def list(self, request):
        query = request.GET.get("query")
        book_id = request.GET.get("book_id")
        decos_join_response = get_decos_join_permit(query=query, book_id=book_id)
        return Response(decos_join_response)

    @extend_schema(
        parameters=permit_request_parameters, description="Request to Decos Join API"
    )
    @action(detail=False)
    def list_documents(self, request):
        query = request.GET.get("query")

        decos_join_response = get_decos_join_request(query=query)

        return Response(decos_join_response)

    @extend_schema(
        parameters=permit_request_parameters, description="Request to Decos Join API"
    )
    @action(detail=False)
    def list_swagger(self, request):
        query = request.GET.get("query")

        decos_join_response = get_decos_join_request_swagger(query=query)

        return Response(decos_join_response)


class CaseTimeLineViewSet(ModelViewSet):
    serializer_class = CaseTimelineSerializer
    queryset = CaseTimelineSubject


class CaseTimeLineThreadViewSet(ModelViewSet):
    serializer_class = CaseTimelineThreadSerializer
    queryset = CaseTimelineThread


class CaseTimeLineReactionViewSet(ModelViewSet):
    serializer_class = CaseTimelineReactionSerializer
    queryset = CaseTimelineReaction


case_identification = OpenApiParameter(
    name="case_identification",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=True,
    description="identification of an OpenZaak Case",
)

subject = OpenApiParameter(
    name="subject",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=True,
    description="Subject of the timeline update",
)

parameters = OpenApiParameter(
    name="parameters",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=True,
    description="Parameters ",
)


thread_request_parameters = [case_identification, subject]


class TimeLineAutomatedViewSet(ViewSet):
    """
    Gateway for automated thread updates
    """

    @extend_schema(
        request=CaseThreadCreationSerializer,
        description=(
            "Request to create a timeline thread object by non humans (auto reporting)"
        ),
    )
    @action(detail=False)
    def add_thread(self, request):
        case = Case.objects.get(identification=request.POST.get("case_identification"))
        case_subject = CaseTimelineSubject.objects.get_or_create(
            subject=request.POST.get("subject"), case=case
        )
        case_thread = CaseTimelineThread(
            subject=case_subject,
            parameters=request.POST.get("parameters"),
            notes=request.POST.get("notes"),
        )

        case_thread.save()
        return case_thread

    @extend_schema(
        request=CaseThreadUpdateSerializer,
        description=(
            "Request to update a timeline thread object by non humans (auto reporting)"
        ),
    )
    @action(detail=False)
    def update_thread(self, request):
        try:
            case_thread = CaseTimelineThread.objects.get(
                id=request.POST.get("thread_id")
            )
        except CaseTimelineThread.DoesNotExist:
            return
        case_thread.parameters = request.POST.get("parameters")
        case_thread.notes = request.POST.get("notes")
        case_thread.save()
        return case_thread
