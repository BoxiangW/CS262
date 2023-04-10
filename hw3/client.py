import threading
import grpc
import time
import os

import chat_pb2 as chat
import chat_pb2_grpc as rpc

PORT = 56789


class Client:

    def __init__(self, server_list):
        self.server_list = server_list
        self.master_index = 1
        self.kill = False
        channel = grpc.insecure_channel(self.server_list[self.master_index])
        self.conn = rpc.ChatServerStub(channel)
        # start the main loop
        self.first_loop()

    def entry_request_iterator(self):
        n = chat.Id(username=self.username)
        while True:
            yield n

    def _start_stream(self):
        # this line will wait for new messages from the server!
        while True:
            if self.kill:
                os._exit(1)
            try:
                for note in self.conn.ChatStream(self.entry_request_iterator()):
                    time.sleep(0.1)  # in case of message display overlap
                    print("[Receive]{}: {}".format(
                        note.username, note.message))
            except:
                self.change_server()

    def send_message(self):
        recipient = input("Enter the recipient's username:\n")
        message = input("Enter the message:\n")
        if not recipient:
            print("Please enter a recipient.")
        elif not message:
            print("Please enter a message.")
        else:
            # create protobug message (called Message)
            n = chat.Message(username=self.username,
                             to=recipient, message=message)
            try:
                # send the Message to the server
                reply = self.conn.SendMessage(n)
                if reply.error:
                    print("[Error]: {}".format(reply.message))
                else:
                    print("[Send]: {}".format(reply.message))
            except grpc.RpcError as e:
                self.change_server()

    def deliver_message(self):
        n = chat.Id(username=self.username)
        try:
            reply = self.conn.SendDeliverMessages(n)
            if reply.error:
                print("[Error]: {}".format(reply.message))
            else:
                print("[Deliver]: {}".format(reply.message))
        except grpc.RpcError as e:
            print(e)
            self.change_server()

    def list_accounts(self):
        wildcard = input("Enter a wildcard (optional):\n")
        if not wildcard:
            wildcard = '*'
        n = chat.ListAccounts(username=self.username, wildcard=wildcard)
        try:
            reply = self.conn.SendListAccounts(n)
            if reply.error:
                print("[Error]: {}".format(reply.message))
            else:
                print("[List]: {}".format(reply.message))
        except grpc.RpcError as e:
            self.change_server()

    def create_account(self):
        username = input("Enter the username to create:\n")
        if not username:
            print("Please enter a username.")
        else:
            n = chat.Id(username=username)
            try:
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
            except:
                self.change_server()

    def delete_account(self):
        n = chat.Id(username=self.username)
        try:
            reply = self.conn.SendDeleteAccount(n)
            if reply.error:
                print("[Error]: {}".format(reply.message))
            else:
                print("[Delete]: {}".format(reply.message))
                self.kill = True
                os._exit(1)
        except grpc.RpcError as e:
            self.change_server()

    def login(self):
        username = input("Enter the username to login:\n")
        if not username:
            print("Please enter a username.")
        else:
            n = chat.Id(username=username)
            try:
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
            except grpc.RpcError as e:
                self.change_server()

    def logout(self):
        n = chat.Id(username=self.username)
        try:
            reply = self.conn.SendLogout(n)
            if reply.error:
                print("[Error]: {}".format(reply.message))
            else:
                print("[Logout]: {}".format(reply.message))
                self.kill = True
                os._exit(1)
        except grpc.RpcError as e:
            self.change_server()

    def first_loop(self):
        print("Available commands:")
        print("1. Create an account")
        print("2. Login to an account")
        print("3. Exit")
        choice = input("Enter a command number (1-3):\n")

        if choice == "1":
            self.create_account()
        elif choice == "2":
            self.login()
        elif choice == "3":
            quit()
        else:
            print("Invalid command. Please try again.")
            self.first_loop()

    def second_loop(self):
        while True:
            print("Available commands:")
            print("1. Send a message")
            print("2. Deliver undelivered message")
            print("3. List accounts")
            print("4. Delete account (and logout)")
            print("5. Logout")
            choice = input("Enter a command number (1-5):\n")

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

    def change_server(self):
        if self.kill:
            os._exit(1)
        try:
            channel = grpc.insecure_channel(
                self.server_list[1])
            self.conn = rpc.ChatServerStub(channel)
            n = chat.Id(username=self.username)
            self.conn.SendHeartbeat(n)
            print('[Switch]: Switched to server 2')
        except:
            channel = grpc.insecure_channel(
                self.server_list[2])
            self.conn = rpc.ChatServerStub(channel)
            n = chat.Id(username=self.username)
            self.conn.SendHeartbeat(n)
            print('[Switch]: Switched to server 3')


if __name__ == '__main__':
    server_list = ['10.250.143.2:56789',
                   '10.250.143.2:56790', '10.250.102.255:56791']
    Client(server_list)
