import threading
import grpc
import time

import chat_pb2 as chat
import chat_pb2_grpc as rpc

PORT = 56789


class Client:

    def __init__(self, host):
        # create a gRPC channel
        channel = grpc.insecure_channel(host + ':' + str(PORT))
        self.conn = rpc.ChatServerStub(channel)
        # start the main loop
        self.first_loop()

    def entry_request_iterator(self):
        while True:
            n = chat.Id(username=self.username)
            yield n

    def _start_stream(self):
        # this line will wait for new messages from the server
        while True:
            for note in self.conn.ChatStream(self.entry_request_iterator()):
                time.sleep(0.1)  # in case of message display overlap
                print("[Receive]{}: {}".format(note.username, note.message))

    def send_message(self):
        recipient = input("Enter the recipient's username: \n")
        message = input("Enter the message: \n")
        if not recipient:
            print("Please enter a recipient.")
        elif not message:
            print("Please enter a message.")
        else:
            # create protobug message (called Message)
            n = chat.Message()
            n.username = self.username
            n.to = recipient
            n.message = message
            reply = self.conn.SendMessage(n)  # send the Message to the server
            if reply.error:
                print("[Error]: {}".format(reply.message))
            else:
                print("[Send]: {}".format(reply.message))

    def deliver_message(self):
        n = chat.DeliverMessages()
        n.username = self.username
        reply = self.conn.SendDeliverMessages(n)
        if reply.error:
            print("[Error]: {}".format(reply.message))
        else:
            print("[Deliver]: {}".format(reply.message))

    def list_accounts(self):
        wildcard = input("Enter a wildcard (optional): \n")
        if not wildcard:
            wildcard = '*'
        n = chat.ListAccounts()
        n.username = self.username
        n.wildcard = wildcard
        reply = self.conn.SendListAccounts(n)
        if reply.error:
            print("[Error]: {}".format(reply.message))
        else:
            print("[List]: {}".format(reply.message))

    def create_account(self):
        username = input("Enter the username to create: \n")
        if not username:
            print("Please enter a username.")
        else:
            n = chat.CreateAccount()
            n.username = username
            reply = self.conn.SendCreateAccount(n)
            if reply.error:
                print("[Error]: {}".format(reply.message))
            else:
                print("[Create]: {}".format(reply.message))
                self.username = username
                # create new listening thread for when new message streams come in
                self.listener = threading.Thread(target=self._start_stream,
                                                 daemon=True)
                self.listener.start()
                self.second_loop()

    def delete_account(self):
        n = chat.DeleteAccount()
        n.username = self.username
        reply = self.conn.SendDeleteAccount(n)
        if reply.error:
            print("[Error]: {}".format(reply.message))
        else:
            print("[Delete]: {}".format(reply.message))
            exit()

    def login(self):
        username = input("Enter the username to login: \n")
        if not username:
            print("Please enter a username.")
        else:
            n = chat.Login()
            n.username = username
            reply = self.conn.SendLogin(n)
            if reply.error:
                print("[Error]: {}".format(reply.message))
            else:
                print("[Login]: {}".format(reply.message))
                self.username = username
                self.listener = threading.Thread(target=self._start_stream,
                                                 daemon=True)
                self.listener.start()
                self.second_loop()

    def logout(self):
        n = chat.Logout()
        n.username = self.username
        reply = self.conn.SendLogout(n)
        if reply.error:
            print("[Error]: {}".format(reply.message))
        else:
            print("[Logout]: {}".format(reply.message))
            exit()

    def first_loop(self):
        while True:
            print("Available commands:")
            print("1. Create an account")
            print("2. Login to an account")
            print("3. Exit")
            choice = input("Enter a command number (1-3): \n")

            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.login()
            elif choice == "3":
                break
            else:
                print("Invalid command. Please try again.")

    def second_loop(self):
        while True:
            print("Available commands:")
            print("1. Send a message")
            print("2. Deliver undelivered message")
            print("3. List accounts")
            print("4. Delete account (and logout)")
            print("5. Logout")
            choice = input("Enter a command number (1-5): \n")

            if choice == "1":
                self.send_message()
            elif choice == "2":
                self.deliver_message()
            elif choice == "3":
                self.list_accounts()
            elif choice == "4":
                self.delete_account()
            elif choice == "5":
                self.logout()
            else:
                print("Invalid command. Please try again.")


if __name__ == '__main__':
    host = input("Enter host ip address: ")
    if not host:
        host = 'localhost'
    Client(host)
