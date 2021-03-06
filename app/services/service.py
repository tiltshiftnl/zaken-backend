from services.connection import Connection


class Service:
    NAME = ""
    DOMAIN = ""
    TYPES = []
    DATA_TYPE = ""

    def __init__(self):
        self.name = self.__get_name__()
        self.domain = self.__get_domain__()
        self.types = self.__get_types__()
        self.data_type = self.__get_data_type__()

    def __get_name__(self):
        if self.NAME == "":
            raise ValueError("Name is not set")

        return self.NAME

    def __get_types__(self):
        if not self.TYPES:
            raise ValueError("Types are not set")

        return self.TYPES

    def __get_domain__(self):
        if self.DOMAIN == "":
            raise ValueError("Domain is not set")

        return self.DOMAIN

    def __get_data_type__(self):
        if self.DATA_TYPE == "":
            raise ValueError("Data type is not set")

        elif self.DATA_TYPE not in self.__get_types__():
            raise ValueError("Data type is not compatible with this domain")

        return self.DATA_TYPE

    def __get_connection__(self):
        return Connection(self.name, self.domain, self.data_type)

    def get(self, uuid=None):
        raise NotImplementedError("Get method not implemented")

    def post(self, **kwargs):
        raise NotImplementedError("Post method not implemented")

    def put(self, uuid=None):
        raise NotImplementedError("Put method not implemented")

    def patch(self, uuid=None):
        raise NotImplementedError("Patch method not implemented")

    def delete(self, uuid=None):
        raise NotImplementedError("Delete method not implemented")

    def publish(self, uuid=None):
        raise NotImplementedError("Publish method not implemented")

    def mock(self):
        raise NotImplementedError("Mock method not implemented")
