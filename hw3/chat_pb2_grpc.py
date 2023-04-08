# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import chat_pb2 as chat__pb2


class ChatServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendMessage = channel.unary_unary(
                '/grpc.ChatServer/SendMessage',
                request_serializer=chat__pb2.Message.SerializeToString,
                response_deserializer=chat__pb2.Reply.FromString,
                )
        self.ChatStream = channel.unary_stream(
                '/grpc.ChatServer/ChatStream',
                request_serializer=chat__pb2.Id.SerializeToString,
                response_deserializer=chat__pb2.Message.FromString,
                )
        self.SendListAccounts = channel.unary_unary(
                '/grpc.ChatServer/SendListAccounts',
                request_serializer=chat__pb2.ListAccounts.SerializeToString,
                response_deserializer=chat__pb2.Reply.FromString,
                )
        self.SendCreateAccount = channel.unary_unary(
                '/grpc.ChatServer/SendCreateAccount',
                request_serializer=chat__pb2.CreateAccount.SerializeToString,
                response_deserializer=chat__pb2.Reply.FromString,
                )
        self.SendDeliverMessages = channel.unary_unary(
                '/grpc.ChatServer/SendDeliverMessages',
                request_serializer=chat__pb2.DeliverMessages.SerializeToString,
                response_deserializer=chat__pb2.Reply.FromString,
                )
        self.SendDeleteAccount = channel.unary_unary(
                '/grpc.ChatServer/SendDeleteAccount',
                request_serializer=chat__pb2.DeleteAccount.SerializeToString,
                response_deserializer=chat__pb2.Reply.FromString,
                )
        self.SendLogin = channel.unary_unary(
                '/grpc.ChatServer/SendLogin',
                request_serializer=chat__pb2.Login.SerializeToString,
                response_deserializer=chat__pb2.Reply.FromString,
                )
        self.SendLogout = channel.unary_unary(
                '/grpc.ChatServer/SendLogout',
                request_serializer=chat__pb2.Logout.SerializeToString,
                response_deserializer=chat__pb2.Reply.FromString,
                )


class ChatServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendMessage(self, request, context):
        """This bi-directional stream makes it possible to send and receive Messages between 2 persons
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ChatStream(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendListAccounts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendCreateAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendDeliverMessages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendDeleteAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendLogin(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendLogout(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChatServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.SendMessage,
                    request_deserializer=chat__pb2.Message.FromString,
                    response_serializer=chat__pb2.Reply.SerializeToString,
            ),
            'ChatStream': grpc.unary_stream_rpc_method_handler(
                    servicer.ChatStream,
                    request_deserializer=chat__pb2.Id.FromString,
                    response_serializer=chat__pb2.Message.SerializeToString,
            ),
            'SendListAccounts': grpc.unary_unary_rpc_method_handler(
                    servicer.SendListAccounts,
                    request_deserializer=chat__pb2.ListAccounts.FromString,
                    response_serializer=chat__pb2.Reply.SerializeToString,
            ),
            'SendCreateAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.SendCreateAccount,
                    request_deserializer=chat__pb2.CreateAccount.FromString,
                    response_serializer=chat__pb2.Reply.SerializeToString,
            ),
            'SendDeliverMessages': grpc.unary_unary_rpc_method_handler(
                    servicer.SendDeliverMessages,
                    request_deserializer=chat__pb2.DeliverMessages.FromString,
                    response_serializer=chat__pb2.Reply.SerializeToString,
            ),
            'SendDeleteAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.SendDeleteAccount,
                    request_deserializer=chat__pb2.DeleteAccount.FromString,
                    response_serializer=chat__pb2.Reply.SerializeToString,
            ),
            'SendLogin': grpc.unary_unary_rpc_method_handler(
                    servicer.SendLogin,
                    request_deserializer=chat__pb2.Login.FromString,
                    response_serializer=chat__pb2.Reply.SerializeToString,
            ),
            'SendLogout': grpc.unary_unary_rpc_method_handler(
                    servicer.SendLogout,
                    request_deserializer=chat__pb2.Logout.FromString,
                    response_serializer=chat__pb2.Reply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'grpc.ChatServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ChatServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.ChatServer/SendMessage',
            chat__pb2.Message.SerializeToString,
            chat__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ChatStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/grpc.ChatServer/ChatStream',
            chat__pb2.Id.SerializeToString,
            chat__pb2.Message.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendListAccounts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.ChatServer/SendListAccounts',
            chat__pb2.ListAccounts.SerializeToString,
            chat__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendCreateAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.ChatServer/SendCreateAccount',
            chat__pb2.CreateAccount.SerializeToString,
            chat__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendDeliverMessages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.ChatServer/SendDeliverMessages',
            chat__pb2.DeliverMessages.SerializeToString,
            chat__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendDeleteAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.ChatServer/SendDeleteAccount',
            chat__pb2.DeleteAccount.SerializeToString,
            chat__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendLogin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.ChatServer/SendLogin',
            chat__pb2.Login.SerializeToString,
            chat__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendLogout(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.ChatServer/SendLogout',
            chat__pb2.Logout.SerializeToString,
            chat__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
