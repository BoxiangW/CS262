import threading

import grpc

import chat_pb2 as chat
import chat_pb2_grpc as rpc

HOST = 'localhost'
PORT = 56789


class Client:

    def __init__(self):
        # create a gRPC channel + stub
        channel = grpc.insecure_channel(HOST + ':' + str(PORT))
        self.conn = rpc.ChatServerStub(channel)
        # start the main loop
        self.loop()

    def __listen_for_messages(self):
        # this line will wait for new messages from the server!
        n = chat.Id()
        n.username = self.username
        for note in self.conn.ChatStream(n):
            print("\nR[{}] {}".format(note.username, note.message))

    def send_message(self):
        try:
            self.username
        except:
            print("Please create your account first")
            return
        recipient = input("Enter the recipient's username: ")
        message = input("Enter the message: ")
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
            # print("S[{}] {}".format(n.name, n.message))  # debugging statement
            reply = self.conn.SendMessage(n)  # send the Message to the server
            if reply.error:
                print("Error: {}".format(reply.message))
            else:
                print(reply.message)

    def list_accounts(self):
        try:
            self.username
        except:
            print("Please create your account first")
            return
        wildcard = input("Enter a wildcard (optional): ")
        if not wildcard:
            wildcard = '*'
        n = chat.ListAccounts(self.username, wildcard)
        reply = self.conn.SendListAccounts(n)
        if reply.error:
            print("Error: {}".format(reply.message))
        else:
            print(reply.message)

    def create_account(self):
        username = input("Enter the username to create: ")
        if not username:
            print("Please enter a username.")
        else:
            self.username = username
            n = chat.CreateAccount()
            n.username = self.username
            reply = self.conn.SendCreateAccount(n)
            if reply.error:
                print("Error: {}".format(reply.message))
            else:
                print(reply.message)

                # create new listening thread for when new message streams come in
                threading.Thread(target=self.__listen_for_messages,
                                 daemon=True).start()

    def delete_account(self):
        try:
            self.username
        except:
            print("Please create your account first")
            return
        n = chat.DeleteAccount()
        n.username = self.username
        reply = self.conn.SendDeleteAccount(n)
        if reply.error:
            print("Error: {}".format(reply.message))
        else:
            print(reply.message)

    def close(self):
        n = chat.Close()
        n.username = self.username
        reply = self.conn.SendClose(n)
        if reply.error:
            print("Error: {}".format(reply.message))
        else:
            print(reply.message)

    def loop(self):
        while True:
            print("Available commands:")
            print("1. Send a message")
            print("2. List accounts")
            print("3. Create an account")
            print("4. Delete an account")
            print("5. Exit")
            choice = input("Enter a command number (1-5): ")

            if choice == "1":
                self.send_message()
            elif choice == "2":
                self.list_accounts()
            elif choice == "3":
                self.create_account()
            elif choice == "4":
                self.delete_account()
            elif choice == "5":
                self.close()
                break
            else:
                print("Invalid command. Please try again.")


if __name__ == '__main__':
    Client()
