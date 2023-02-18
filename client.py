import socket
import json
import threading
import time
import sys

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

class ChatClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((server_host, server_port))
        self.username = None

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

    def close(self):
        self.sock.sendall(create_msg("close", self.username))
        self.sock.close()


# Interactive script below
PORT=56789

# Create an instance of the ChatClient class
client = ChatClient("localhost", PORT)

# handles user interaction
def handle_user():
    # Loop until the user chooses to exit
    while True:
        # Print the available commands
        print("Available commands:")
        print("1. Send a message")
        print("2. List accounts")
        print("3. Create an account")
        print("4. Delete an account")
        print("5. Exit")

        # Prompt the user for input
        choice = input("Enter a command number (1-6): ")

        # Call the appropriate client function based on the user input
        if choice == "1":
            recipient = input("Enter the recipient's username: ")
            message = input("Enter the message: ")
            client.send_message(recipient, message)
        elif choice == "2":
            username = input("Enter a username (optional): ")
            client.list_accounts(username)
        elif choice == "3":
            username = input("Enter the username to create: ")
            client.create_account(username)
        elif choice == "4":
            client.delete_account()
        elif choice == "5":
            client.close()
            break
        else:
            print("Invalid command. Please try again.")

def handle_message():
    while True:
        msg = client.sock.recv(1024).decode()
        if not msg:
            break
        msg = json.loads(msg)

        if msg["cmd"] == "deliver":
            print("{} sent: {}".format(msg["from"], msg["body"]))
        elif msg["cmd"] == "create":
            if msg["error"]:
                print("Failed to create account: {}. Please try again.".format(msg["body"]))
            else:
                print("Account created successfully.")
                client.username = msg["to"]
        elif msg["cmd"] == "delete":
            if msg["error"]:
                print("Failed to delete account: {}. Please try again.".format(msg["body"]))
            else:
                print("Account deleted successfully.")
                client.username = None
        elif msg["cmd"] == "list":
            print(json.dumps(msg["body"], indent=2))
        elif msg["cmd"] == "send":
            if msg["error"]:
                print("Failed to send message: {}. Please try again.".format(msg["body"]))
            else:
                print(msg["body"])

# this function requests for a msg delivery every 5 sec
def request_deliver():
    while True:
        if client.username:
            client.receive_messages()
            time.sleep(5.0)


if __name__ == '__main__':
    threading.Thread(target=handle_user).start()
    threading.Thread(target=handle_message).start()
    threading.Thread(target=request_deliver).start()