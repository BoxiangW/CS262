import socket
import json
import threading
import time
import sys
import os

import datetime

# Maximum message buffer size
MSGLEN = 409600

# a function for printing to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# a message generator function
def create_msg(cmd, src="", to="", body=""):
    msg = {
        "cmd": cmd,
        "from": src,
        "to": to,
        "body": body
    }
    return json.dumps(msg).encode()

# class for the client
class ChatClient:

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((server_host, server_port))
        self.username = None
        self.login_err = False

    def login(self, username):
        if self.username is None:
            self.sock.sendall(create_msg("login", username))
        else:
            eprint("You already logged in")

    def send_message(self, recipient, message):
        if not self.username:
            eprint("Please create your username first")
        else:
            self.sock.sendall(create_msg("send", self.username, recipient, message))

    def list_accounts(self, wildcard):
        self.sock.sendall(create_msg("list", self.username, body=wildcard))

    def create_account(self, username):
        self.sock.sendall(create_msg("create", username))

    def delete_account(self):
        self.sock.sendall(create_msg("delete", self.username))

    def receive_messages(self):
        self.sock.sendall(create_msg("deliver", self.username))

    def log_off(self):
        self.sock.sendall(create_msg("logoff", src=self.username))

    def close(self):
        self.sock.sendall(create_msg("close", self.username))
        self.sock.close()


# Interactive script below
PORT=56789

# Create an instance of the ChatClient class
host = input("Enter host ip address: ")
client = ChatClient(host, PORT)

# handles user interaction
def handle_user():
    # Loop until the user chooses to exit
    while True:
        print("Available commands:")
        if not client.username:
            print("0. Login")
            print("1. Create an account")
            print("2. Exit")

            # Prompt the user for input
            choice = input("Enter a command number (0-2): ")

            # Call the appropriate client function based on the user input
            if choice == "0":
                username = input("Enter your username: ")
                client.login(username)
                while not client.username:
                    if client.login_err:
                        client.login_err = False
                        break

            elif choice == "1":
                username = input("Enter the username to create: ")
                client.create_account(username)
            elif choice == "2":
                client.close()
                os._exit(1)
            else:
                print("Invalid command. Please try again.")

        else:
            # Print the available commands
            print("0. Send a message")
            print("1. Deliver undelivered messages")
            print("2. List accounts")
            print("3. Delete an account")
            print("4. Log off")

            # Prompt the user for input
            choice = input("Enter a command number (0-4): ")

            # Call the appropriate client function based on the user input
            if choice == "0":
                recipient = input("Enter the recipient's username: ")
                message = input("Enter the message: ")
                print(datetime.datetime.now())
                client.send_message(recipient, message)
            elif choice == "1":
                request_deliver()
            elif choice == "2":
                username = input("Enter a matching wildcard (optional): ")
                client.list_accounts(username)
            elif choice == "3":
                client.delete_account()
            elif choice == "4":
                client.log_off()
                client.username = None
            else:
                print("Invalid command. Please try again.")


def handle_message():
    while True:
        msg = client.sock.recv(MSGLEN).decode()
        if not msg:
            break
        msg = json.loads(msg)

        if msg["cmd"] == "login":
            if msg["error"]:
                client.login_err = True
                print("Failed to login: {}. Please try again.".format(msg["body"]))
            else:
                print("Logged in successfully.")
                client.username = msg["to"]
        elif msg["cmd"] == "deliver":
            print("{} sent: {}".format(msg["from"], msg["body"]))
            print(datetime.datetime.now())
        elif msg["cmd"] == "create":
            if msg["error"]:
                print("Failed to create account: {}. Please try again.".format(msg["body"]))
            else:
                print("Account created successfully.")
        elif msg["cmd"] == "delete":
            if msg["error"]:
                print("Failed to delete account: {}. Please try again.".format(msg["body"]))
            else:
                print("Account deleted successfully.")
                client.username = None
        elif msg["cmd"] == "list":
            print(json.dumps(msg["body"], indent=2))
        elif msg["cmd"] == "send":
            # print(datetime.datetime.now())
            if msg["error"]:
                print("Failed to send message: {}. Please try again.".format(msg["body"]))
            else:
                print(msg["body"])
        elif msg["cmd"] == "logoff":
            print(msg["body"])

# this function requests for a msg delivery every 5 sec
def request_deliver():
    if client.username:
        client.receive_messages()


threading.Thread(target=handle_user).start()
threading.Thread(target=handle_message).start()
# threading.Thread(target=request_deliver).start()