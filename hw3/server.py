from concurrent import futures

import grpc
import time
import fnmatch
import pickle
import sys

import chat_pb2 as chat
import chat_pb2_grpc as rpc

DEBUG = False


class ChatServer(rpc.ChatServerServicer):
    """Class representing a single server for hw 3.

    Attributes:
        server_list: A list of string contains servers' ip address and port number.
        server_id: An integer indicates current master server.
        bin_file: A string of the bin file name.
        accounts: A dict of accounts' details including online status and undelivered messages.
        logout_accounts: A dict of undelivered messages for logged out accounts.
        servers: A list of connection with other servers.
        is_master: A boolean indicates whether is master itself.
    """

    def __init__(self, server_list, server_id, restart):
        """Initializes the instance with basic settings.

        Args:
          server_list: Used to send messages to all the possible master servers.
          server_id: Used to identify the server.
          restart: Used to determine whether to restart from persisted file.
        """
        self.server_list = server_list
        self.server_id = server_id
        self.bin_file = "log_" + str(self.server_id) + ".bin"
        self.accounts = {}  # {username: [status, [chat.Message]]}
        self.logout_accounts = {}  # {username: [chat.Message]}

        if restart:
            try:
                self.readPersist()
                print("[Start] Server restarted from persisted file.")
            except FileNotFoundError:
                self.persist()
                print("[Start] No persist file found. Blank server created.")
        else:
            self.persist()
            print("[Start] Blank server created.")

        self.servers = []
        for i in range(len(self.server_list)):
            if i != self.server_id:
                channel = grpc.insecure_channel(
                    server_list[i])
                conn = rpc.ChatServerStub(channel)
                self.servers.append(conn)
            else:
                self.servers.append(None)

        if self.server_id == 0:
            self.is_master = True
            print("[Status] Master")
        else:
            self.is_master = False
            print("[Status] Slave")

    def ChatStream(self, request_iterator: chat.Id, context) -> chat.Message:
        """Bidirectional streaming RPC for continuously deliver messages.

        Args:
          request_iterator: An iterator of chat.Id.
          context: A grpc context. See chat_pb2_grpc.py for more details.
        """
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while True:
            # Check if there are any new messages
            for request in request_iterator:
                if self.accounts[request.username][0]:
                    while len(self.accounts[request.username][1]) > 0:
                        # wait for all servers to respond
                        for i, server in enumerate(self.servers):
                            if server:
                                # try:
                                #     reply = server.UpdateMessage(request)
                                # except grpc.RpcError as e:
                                #     continue
                                while True:
                                    try:
                                        reply = server.UpdateMessage(request)
                                    except grpc.RpcError as e:
                                        break
                                    else:
                                        if reply.error:
                                            break
                        n = self.accounts[request.username][1].pop(0)
                        self.persist()
                        yield n

    def UpdateMessage(self, request: chat.Id, context) -> chat.Reply:
        """Unary RPC for slave servers to update remaining messages.

        Args:
          request: An iterator of chat.Id.
          context: A grpc context. See chat_pb2_grpc.py for more details.
        """
        if len(self.accounts[request.username][1]) > 0:
            self.accounts[request.username][1].pop(0)
            n = chat.Reply(message="Message updated", error=False)
            self.persist()
        else:
            n = chat.Reply(message="Message not updated", error=True)
        return n

    def SendMessage(self, request: chat.Message, context) -> chat.Reply:
        """Unary RPC for store messages in servers.

        Args:
          request: chat.Message contains message details including sender, receiver and message.
          context: A grpc context. See chat_pb2_grpc.py for more details.
        """
        if request.to not in self.accounts:
            n = chat.Reply(message="Recipient not registered", error=True)
        else:
            print("[Message] {} to {}: {}".format(
                request.username, request.to, request.message))
            if self.accounts[request.to][0]:
                self.accounts[request.to][1].append(request)
                self.persist()
            else:
                self.logout_accounts[request.to].append(request)
                self.persist()
            n = chat.Reply(message="Message sent", error=False)

        # wait for all servers to respond
        if self.is_master:
            for i, server in enumerate(self.servers):
                if server:
                    try:
                        reply = server.SendMessage(request)
                        if reply != n:
                            print(f"Error on server {i}")
                    except grpc.RpcError as e:
                        continue
        return n

    def SendListAccounts(self, request: chat.ListAccounts, context) -> chat.Reply:
        """Unary RPC for requesting list of accounts with optional wildcards.

        Args:
          request: chat.Message contains details including sender username, and optional wildcard.
          context: A grpc context. See chat_pb2_grpc.py for more details.
        """
        print("[List] {}: {}".format(request.username, request.wildcard))
        matching_accounts = fnmatch.filter(
            list(self.accounts.keys()), request.wildcard)
        matching_accounts = ", ".join(matching_accounts)
        n = chat.Reply(message=matching_accounts, error=False)

        # wait for all servers to respond
        if self.is_master:
            for i, server in enumerate(self.servers):
                if server is not None:
                    try:
                        reply = server.SendListAccounts(request)
                        if reply != n:
                            print(f"Error on server {i}")
                    except grpc.RpcError as e:
                        continue

        return n

    def SendCreateAccount(self, request: chat.Id, context) -> chat.Reply:
        """Unary RPC for creating accounts.

        Args:
          request: chat.Id contains sender username.
          context: A grpc context. See chat_pb2_grpc.py for more details.
        """
        print("[Create] {}".format(request.username))
        if request.username in self.accounts:
            n = chat.Reply(message="Username already taken", error=True)
        else:
            self.accounts[request.username] = [True, []]
            n = chat.Reply(message="Account created", error=False)
            self.persist()

        # wait for all servers to respond
        if self.is_master:
            for i, server in enumerate(self.servers):
                if server is not None:
                    try:
                        reply = server.SendCreateAccount(request)
                        if reply != n:
                            print(f"Error on server {i}")
                    except grpc.RpcError as e:
                        continue
        return n

    def SendDeliverMessages(self, request: chat.Id, context) -> chat.Reply:
        """Unary RPC for requesting a delivery of undelivered messages.

        Args:
          request: chat.Id contains sender username.
          context: A grpc context. See chat_pb2_grpc.py for more details.
        """
        try:
            self.logout_accounts[request.username]
        except:
            n = chat.Reply(message="No messages to deliver", error=True)
        else:
            self.accounts[request.username][1] += self.logout_accounts[request.username]
            del self.logout_accounts[request.username]
            print("[Deliver] {}".format(request.username))
            n = chat.Reply(message="Messages delivered", error=False)
            self.persist()

        # wait for all servers to respond
        if self.is_master:
            for i, server in enumerate(self.servers):
                if server is not None:
                    try:
                        reply = server.SendDeliverMessages(request)
                        if reply != n:
                            print(f"Error on server {i}")
                    except grpc.RpcError as e:
                        continue
        return n

    def SendDeleteAccount(self, request: chat.Id, context) -> chat.Reply:
        """Unary RPC for deleting accounts.

        Args:
          request: chat.Id contains sender username.
          context: A grpc context. See chat_pb2_grpc.py for more details.
        """
        try:
            self.logout_accounts[request.username]
        except:
            del self.accounts[request.username]
            print("[Delete] {}".format(request.username))
            n = chat.Reply(message="Account deleted", error=False)
            self.persist()

        else:
            if len(self.logout_accounts[request.username]) > 0:
                n = chat.Reply()
                n.message = "You have messages to deliver"
                n.error = True
            else:
                del self.accounts[request.username]
                print("[Delete] {}".format(request.username))
                n = chat.Reply(message="Account deleted", error=False)
                self.persist()

        # wait for all servers to respond
        if self.is_master:
            for i, server in enumerate(self.servers):
                if server is not None:
                    try:
                        reply = server.SendDeleteAccount(request)
                        if reply != n:
                            print(f"Error on server {i}")
                    except grpc.RpcError as e:
                        continue
        return n

    def SendLogin(self, request: chat.Id, context) -> chat.Reply:
        """Unary RPC for accounts login.

        Args:
          request: chat.Id contains sender username.
          context: A grpc context. See chat_pb2_grpc.py for more details.
        """
        if request.username not in self.accounts:
            n = chat.Reply(message="Username not found", error=True)
        elif self.accounts[request.username][0] == True:
            n = chat.Reply(message="Already logged in", error=True)
        else:
            self.accounts[request.username][0] = True
            print("[Login] {}".format(request.username))
            n = chat.Reply(message="Login successful", error=False)
            self.persist()

        # wait for all servers to respond
        if self.is_master:
            for i, server in enumerate(self.servers):
                if server is not None:
                    try:
                        reply = server.SendLogin(request)
                        if reply != n:
                            print(f"Error on server {i}")
                    except grpc.RpcError as e:
                        continue
        return n

    def SendLogout(self, request: chat.Id, context) -> chat.Reply:
        """Unary RPC for accounts logout.

        Args:
          request: chat.Id contains sender username.
          context: A grpc context. See chat_pb2_grpc.py for more details.
        """
        self.accounts[request.username][0] = False
        self.logout_accounts[request.username] = []
        print("[Logout] {}".format(request.username))
        n = chat.Reply(message="Logout successful", error=False)
        self.persist()

        # wait for all servers to respond
        if self.is_master:
            for i, server in enumerate(self.servers):
                if server is not None:
                    try:
                        reply = server.SendLogout(request)
                        if reply != n:
                            print(f"Error on server {i}")
                    except grpc.RpcError as e:
                        continue
        return n

    def SendHeartbeat(self, request: chat.Id, context) -> chat.Reply:
        """Unary RPC for server status transformation.

        Args:
          request: chat.Id contains sender username.
          context: A grpc context. See chat_pb2_grpc.py for more details.
        """
        if request.leader:
            self.is_master = True
            print("[Status] Master")
        else:
            self.is_master = False
            print("[Status] Slave")

        if self.is_master:
            for i, server in enumerate(self.servers):
                if server is not None:
                    try:
                        n = chat.StatusChange(leader=False)
                        reply = server.SendHeartbeat(n)
                    except grpc.RpcError as e:
                        continue
        return chat.Reply(message="Heartbeat received", error=False)

    def persist(self):
        """Persist the accounts and logout_accounts dictionaries to a binary file."""
        with open(self.bin_file, "wb") as outfile:
            pickle.dump(self.accounts, outfile)
            pickle.dump(self.logout_accounts, outfile)

        if DEBUG:
            print(self.accounts)
            print(self.logout_accounts)

    def readPersist(self):
        """Read the accounts and logout_accounts dictionaries from a binary file."""
        with open(self.bin_file, "rb") as infile:
            self.accounts = pickle.load(infile)
            self.logout_accounts = pickle.load(infile)


if __name__ == '__main__':
    # Read server Id
    server_list = ['10.250.143.2:56789',
                   '10.250.143.2:56790', '10.250.102.255:56791']
    server_id = int(sys.argv[1])
    restart = int(sys.argv[2])
    # the workers is like the amount of threads that can be opened at the same time, when there are 10 clients connected
    # then no more clients able to connect to the server.
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=10))
    rpc.add_ChatServerServicer_to_server(
        ChatServer(server_list, server_id, restart), server)  # register the server to gRPC
    # gRPC basically manages all the threading and server responding logic, which is perfect!
    print(
        f'[Address] Starting server at {server_list[server_id]}. Listening...')
    server.add_insecure_port(server_list[server_id])
    server.start()
    # Server starts in background (in another thread) so keep waiting
    # if we don't wait here the main thread will end, which will end all the child threads, and thus the threads
    # from the server won't continue to work and stop the server
    while True:
        time.sleep(64 * 64 * 100)
