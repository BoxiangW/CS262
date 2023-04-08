from concurrent import futures

import grpc
import time
import fnmatch
import pickle

import chat_pb2 as chat
import chat_pb2_grpc as rpc

PORT = 56789

FILENAME = 'log.bin'

class ChatServer(rpc.ChatServerServicer):

    def __init__(self):
        # List with all the chat history
        self.chats = []
        # List with all the accounts
        self.accounts = {}  # {username: [status, [chat.Message]]}
        self.logout_accounts = {}  # {username: [chat.Message]}
        self.log = []
        self.read_log_from_file()
        self.parse_log()

    # The stream which will be used to send new messages to clients
    def ChatStream(self, request, context):
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while True:
            # Check if there are any new messages
            time.sleep(0.1)
            if self.accounts[request.username][0]:
                while len(self.accounts[request.username][1]) > 0:
                    n = self.accounts[request.username][1].pop(0)
                    self.log.append(("POP", request))
                    self.log_to_file()
                    yield n

    def SendMessage(self, request: chat.Message, context):
        # this is only for the server console
        print("[Message] {} to {}: {}".format(
            request.username, request.to, request.message))
        # Add it to the chat history
        if request.to not in self.accounts:
            n = chat.Reply()
            n.message = "Recipient not registered"
            n.error = True
            return n
        else:
            self.chats.append(request)

            if self.accounts[request.to][0]:
                self.accounts[request.to][1].append(request)
                self.log.append(("ADD", request))
                self.log_to_file()
            else:
                self.logout_accounts[request.to].append(request)
                self.log.append(("LOGOUT_ADD", request))
                self.log_to_file()

            n = chat.Reply()
            n.message = "Message sent"
            n.error = False

            return n

    def SendListAccounts(self, request: chat.ListAccounts, context):
        # this is only for the server console
        print("[List] {}: {}".format(request.username, request.wildcard))
        matching_accounts = fnmatch.filter(
            list(self.accounts.keys()), request.wildcard)
        matching_accounts = ", ".join(matching_accounts)
        n = chat.Reply()
        n.message = matching_accounts
        n.error = False
        print("[List] {}: {}".format(request.wildcard, matching_accounts))
        
        return n

    def SendCreateAccount(self, request: chat.CreateAccount, context):
        # this is only for the server console
        print("[Create] {}".format(request.username))
        if request.username in self.accounts:
            n = chat.Reply()
            n.message = "Username already taken"
            n.error = True
            return n
        else:
            self.accounts[request.username] = [True, []]
            n = chat.Reply()
            n.message = "Account created"
            n.error = False

            self.log.append(("ACC_CREATE", request))
            self.log_to_file()
            return n

    def SendDeliverMessages(self, request, context):
        print("[Deliver] {}".format(request.username))
        try:
            self.logout_accounts[request.username]
        except:
            n = chat.Reply()
            n.message = "No messages to deliver"
            n.error = True
            return n
        else:
            self.accounts[request.username][1] += self.logout_accounts[request.username]
            del self.logout_accounts[request.username]
            n = chat.Reply()
            n.message = "Messages delivered"
            n.error = False

            self.log.append(("SEND_DELIVER", request))
            self.log_to_file()
            return n

    def SendDeleteAccount(self, request: chat.DeleteAccount, context):
        # this is only for the server console
        try:
            self.logout_accounts[request.username]
        except:
            del self.accounts[request.username]
            print("[Delete] {}".format(request.username))
            n = chat.Reply()
            n.message = "Account deleted"
            n.error = False

            self.log.append(("ACC_DEL", request))
            self.log_to_file()
            return n
        else:
            if len(self.logout_accounts[request.username]) > 0:
                n = chat.Reply()
                n.message = "You have messages to deliver"
                n.error = True
                return n

    def SendLogin(self, request: chat.Login, context):
        # this is only for the server console
        if request.username not in self.accounts:
            n = chat.Reply()
            n.message = "Username not found"
            n.error = True
            return n
        elif self.accounts[request.username][0] == True:
            n = chat.Reply()
            n.message = "Already logged in"
            n.error = True
            return n
        else:
            self.accounts[request.username][0] = True
            print("[Login] {}".format(request.username))
            n = chat.Reply()
            n.message = "Login successful"
            n.error = False

            self.log.append(("LOGIN", request))
            self.log_to_file()
            return n

    def SendLogout(self, request: chat.Logout, context):
        # this is only for the server console
        self.accounts[request.username][0] = False
        self.logout_accounts[request.username] = []
        print("[Logout] {}".format(request.username))
        n = chat.Reply()
        n.message = "Logout successful"
        n.error = False

        self.log.append(("LOGOUT", request))
        self.log_to_file()
        return n

    # something needs to be returned required by protobuf language, we just return empty msg

    def log_to_file(self):
        with open(FILENAME, "ab+") as f:
            pickle.dump(self.log[-1], f)

        # # Debug only:
        # print(self.chats)
        # print(self.accounts)
        # print(self.logout_accounts)

    def read_log_from_file(self):
        try:
            with open(FILENAME, "rb") as f:
                while True:
                    try:
                        request = pickle.load(f)
                        # process obj here
                        self.log.append(request)
                    except EOFError:
                        break
        except IOError:
            return

    def parse_log(self):
        for tup in self.log:
            status = tup[0]
            req = tup[1]
            if status == "ADD":
                self.chats.append(req)
                self.accounts[req.to][1].append(req)
            elif status == "ACC_CREATE":
                self.accounts[req.username] = [True, []]
            elif status == "SEND_DELIVER":
                self.accounts[req.username][1] += self.logout_accounts[req.username]
                del self.logout_accounts[req.username]
            elif status == "ACC_DEL":
                del self.accounts[req.username]
            elif status == "LOGIN":
                self.accounts[req.username][0] = True
            elif status == "LOGOUT":
                self.accounts[req.username][0] = False
                self.logout_accounts[req.username] = []
            elif status == "LOGOUT_ADD": # if msg was sent to an offline user, store that to their queue
                self.chats.append(req)
                self.logout_accounts[req.to].append(req)
            elif status == "POP":
                self.accounts[req.username][1].pop(0)

        # Make sure everyone is logged out at start
        for key in self.accounts:
            self.accounts[key][0] = False

        # Debug only:
        print(self.chats)
        print(self.accounts)
        print(self.logout_accounts)
    
            
if __name__ == '__main__':
    # the workers is like the amount of threads that can be opened at the same time, when there are 10 clients connected
    # then no more clients able to connect to the server.
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=10))  # create a gRPC server
    rpc.add_ChatServerServicer_to_server(
        ChatServer(), server)  # register the server to gRPC
    # gRPC basically manages all the threading and server responding logic, which is perfect!
    print('Starting server. Listening...')
    server.add_insecure_port('[::]:' + str(PORT))
    server.start()
    # Server starts in background (in another thread) so keep waiting
    # if we don't wait here the main thread will end, which will end all the child threads, and thus the threads
    # from the server won't continue to work and stop the server
    while True:
        time.sleep(64 * 64 * 100)
