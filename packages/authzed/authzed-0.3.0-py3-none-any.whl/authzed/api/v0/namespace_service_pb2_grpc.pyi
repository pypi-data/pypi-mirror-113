"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import grpc

from .namespace_service_pb2 import *
class NamespaceServiceStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    ReadConfig:grpc.UnaryUnaryMultiCallable[
        global___ReadConfigRequest,
        global___ReadConfigResponse] = ...

    WriteConfig:grpc.UnaryUnaryMultiCallable[
        global___WriteConfigRequest,
        global___WriteConfigResponse] = ...


class NamespaceServiceServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def ReadConfig(self,
        request: global___ReadConfigRequest,
        context: grpc.ServicerContext,
    ) -> global___ReadConfigResponse: ...

    @abc.abstractmethod
    def WriteConfig(self,
        request: global___WriteConfigRequest,
        context: grpc.ServicerContext,
    ) -> global___WriteConfigResponse: ...


def add_NamespaceServiceServicer_to_server(servicer: NamespaceServiceServicer, server: grpc.Server) -> None: ...
