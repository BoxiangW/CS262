import unittest
import threading
import socket
import time
import json

from server import ChatServer

# define host and port for server
HOST = 'localhost'
PORT = 56789


class TestChatServer(unittest.TestCase):

    def setUp(self):
        self.server = ChatServer(HOST, PORT)
        # start server in a new thread
        self.server_thread = threading.Thread(target=self.server.start)
        self.server_thread.start()

    def tearDown(self):
        # stop server and join thread
        self.server.stop()
        self.server_thread.join()

    def test_login(self):
        # test login command with valid credentials
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((HOST, PORT))
            msg = {"cmd": "login", "from": "alice", "body": "password123"}
            client.sendall(str.encode(f"{len(str(msg)):<{10}}{str(msg)}"))
            data = client.recv(4096)
            self.assertEqual(json.loads(data.decode()), {"cmd": "login", "to": "alice", "body": "Login successful", "from": "", "error": False})

    def test_create_and_list(self):
        # test create and list commands
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((HOST, PORT))
            # create account
            msg = {"cmd": "create", "from": "bob", "body": "password456"}
            client.sendall(str.encode(f"{len(str(msg)):<{10}}{str(msg)}"))
            data = client.recv(4096)
            self.assertEqual(json.loads(data.decode()), {"cmd": "create", "to": "bob", "body": "Account created", "from": "", "error": False})
            # list accounts
            msg = {"cmd": "list", "from": "bob", "body": "*"}
            client.sendall(str.encode(f"{len(str(msg)):<{10}}{str(msg)}"))
            data = client.recv(4096)
            self.assertEqual(json.loads(data.decode()), {"cmd": "list", "to": "bob", "body": "alice,bob", "from": "", "error": False})

    def test_send_and_deliver(self):
        # test send and deliver commands
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client1, socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client2:
            client1.connect((HOST, PORT))
            client2.connect((HOST, PORT))
            # login
            msg = {"cmd": "login", "from": "alice", "body": "password123"}
            client1.sendall(str.encode(f"{len(str(msg)):<{10}}{str(msg)}"))
            data = client1.recv(4096)
            self.assertEqual(json.loads(data.decode()), {"cmd": "login", "to": "alice", "body": "Login successful", "from": "", "error": False})
            # send message
            msg = {"cmd": "send", "from": "alice", "to": "bob", "body": "Hello, Bob!"}
            client1.sendall(str.encode(f"{len(str(msg)):<{10}}{str(msg)}"))
            data = client1.recv(4096)
            self.assertEqual(json.loads(data.decode()), {"cmd": "send", "to": "", "body": "Message sent", "from": "", "error": False})
            # deliver message
            msg = {"cmd": "deliver", "from": "bob", "body": ""}
           
