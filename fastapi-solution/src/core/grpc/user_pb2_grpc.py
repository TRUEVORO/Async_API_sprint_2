# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import user_pb2 as user__pb2


class DetailerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.DetailsByToken = channel.unary_unary(
            '/Detailer/DetailsByToken',
            request_serializer=user__pb2.UserTokenRequest.SerializeToString,
            response_deserializer=user__pb2.UserResponse.FromString,
        )


class DetailerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def DetailsByToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DetailerServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'DetailsByToken': grpc.unary_unary_rpc_method_handler(
            servicer.DetailsByToken,
            request_deserializer=user__pb2.UserTokenRequest.FromString,
            response_serializer=user__pb2.UserResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler('Detailer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Detailer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def DetailsByToken(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Detailer/DetailsByToken',
            user__pb2.UserTokenRequest.SerializeToString,
            user__pb2.UserResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
