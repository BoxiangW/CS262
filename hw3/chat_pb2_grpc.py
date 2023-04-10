# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import chat_pb2 as chat__pb2


class ChatServerStub(object):
    """Server for hw3
    """

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
        self.ChatStream = channel.stream_stream(
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
                request_serializer=chat__pb2.Id.SerializeToString,
                response_deserializer=chat__pb2.Reply.FromString,
                )
        self.SendDeliverMessages = channel.unary_unary(
                '/grpc.ChatServer/SendDeliverMessages',
                request_serializer=chat__pb2.Id.SerializeToString,
                response_deserializer=chat__pb2.Reply.FromString,
                )
        self.SendDeleteAccount = channel.unary_unary(
                '/grpc.ChatServer/SendDeleteAccount',
                request_serializer=chat__pb2.Id.SerializeToString,
                response_deserializer=chat__pb2.Reply.FromString,
                )
        self.SendLogin = channel.unary_unary(
                '/grpc.ChatServer/SendLogin',
                request_serializer=chat__pb2.Id.SerializeToString,
                response_deserializer=chat__pb2.Reply.FromString,
                )
        self.SendLogout = channel.unary_unary(
                '/grpc.ChatServer/SendLogout',
                request_serializer=chat__pb2.Id.SerializeToString,
                response_deserializer=chat__pb2.Reply.FromString,
                )
        self.SendHeartbeat = channel.unary_unary(
                '/grpc.ChatServer/SendHeartbeat',
                request_serializer=chat__pb2.StatusChange.SerializeToString,
                response_deserializer=chat__pb2.Reply.FromString,
                )
        self.UpdateMessage = channel.unary_unary(
                '/grpc.ChatServer/UpdateMessage',
                request_serializer=chat__pb2.Id.SerializeToString,
                response_deserializer=chat__pb2.Reply.FromString,
                )


class ChatServerServicer(object):
    """Server for hw3
    """

    def SendMessage(self, request, context):
        """send a message to a user
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ChatStream(self, request_iterator, context):
        """stream of messages for a user
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendListAccounts(self, request, context):
        """list all accounts
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendCreateAccount(self, request, context):
        """create an account
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendDeliverMessages(self, request, context):
        """deliver messages to a user
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendDeleteAccount(self, request, context):
        """delete an account
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendLogin(self, request, context):
        """login to an account
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendLogout(self, request, context):
        """logout of an account
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendHeartbeat(self, request, context):
        """send a heartbeat to transfer slave to master or master to slave
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateMessage(self, request, context):
        """update message to slave server
        """
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
            'ChatStream': grpc.stream_stream_rpc_method_handler(
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
                    request_deserializer=chat__pb2.Id.FromString,
                    response_serializer=chat__pb2.Reply.SerializeToString,
            ),
            'SendDeliverMessages': grpc.unary_unary_rpc_method_handler(
                    servicer.SendDeliverMessages,
                    request_deserializer=chat__pb2.Id.FromString,
                    response_serializer=chat__pb2.Reply.SerializeToString,
            ),
            'SendDeleteAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.SendDeleteAccount,
                    request_deserializer=chat__pb2.Id.FromString,
                    response_serializer=chat__pb2.Reply.SerializeToString,
            ),
            'SendLogin': grpc.unary_unary_rpc_method_handler(
                    servicer.SendLogin,
                    request_deserializer=chat__pb2.Id.FromString,
                    response_serializer=chat__pb2.Reply.SerializeToString,
            ),
            'SendLogout': grpc.unary_unary_rpc_method_handler(
                    servicer.SendLogout,
                    request_deserializer=chat__pb2.Id.FromString,
                    response_serializer=chat__pb2.Reply.SerializeToString,
            ),
            'SendHeartbeat': grpc.unary_unary_rpc_method_handler(
                    servicer.SendHeartbeat,
                    request_deserializer=chat__pb2.StatusChange.FromString,
                    response_serializer=chat__pb2.Reply.SerializeToString,
            ),
            'UpdateMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateMessage,
                    request_deserializer=chat__pb2.Id.FromString,
                    response_serializer=chat__pb2.Reply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'grpc.ChatServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ChatServer(object):
    """Server for hw3
    """

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
    def ChatStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/grpc.ChatServer/ChatStream',
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
            chat__pb2.Id.SerializeToString,
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
            chat__pb2.Id.SerializeToString,
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
            chat__pb2.Id.SerializeToString,
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
            chat__pb2.Id.SerializeToString,
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
            chat__pb2.Id.SerializeToString,
            chat__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendHeartbeat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.ChatServer/SendHeartbeat',
            chat__pb2.StatusChange.SerializeToString,
            chat__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.ChatServer/UpdateMessage',
            chat__pb2.Id.SerializeToString,
            chat__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
