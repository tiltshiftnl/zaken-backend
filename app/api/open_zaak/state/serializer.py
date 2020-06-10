from rest_framework import serializers

class StateSerializer(serializers.Serializer):
    url = serializers.URLField(read_only=True)
    uuid = serializers.CharField(read_only=True)