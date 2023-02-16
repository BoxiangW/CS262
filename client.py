import socket
import json

class ChatClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((server_host, server_port))

    def send_message(self, recipient, message):
        request = {
            "type": "message",
            "recipient": recipient,
            "message": message
        }
        self.sock.sendall(json.dumps(request).encode())

    def list_accounts(self, username=""):
        request = {
            "type": "list",
            "username": username
        }
        self.sock.sendall(json.dumps(request).encode())
        response = self.sock.recv(1024).decode()
        return json.loads(response)

    def create_account(self, username):
        request = {
            "type": "create",
            "username": username
        }
        self.sock.sendall(json.dumps(request).encode())
        response = self.sock.recv(1024).decode()
        return json.loads(response)

    def delete_account(self, username):
        request = {
            "type": "delete",
            "username": username
        }
        self.sock.sendall(json.dumps(request).encode())
        response = self.sock.recv(1024).decode()
        return json.loads(response)

    def receive_messages(self, username):
        request = {
            "type": "deliver",
            "username": username
        }
        self.sock.sendall(json.dumps(request).encode())
        response = self.sock.recv(1024).decode()
        return json.loads(response)

    def close(self):
        self.sock.close()
