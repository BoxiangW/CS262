import unittest
import threading
import socket
import time
import json
import os
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
        

    def test_create_and_list(self):
        # test create and list commands
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        # create account alice
        msg = {"cmd": "create", "from": "alice", "to": "", "body": ""}
        client.sendall(json.dumps(msg).encode())
        data = client.recv(4096)
        self.assertEqual(json.loads(data.decode()), {"cmd": "create", "to": "alice", "body": "Account created", "from": "", "error": False})
        # create account bob
        msg = {"cmd": "create", "from": "bob", "to": "", "body": ""}
        client.sendall(json.dumps(msg).encode())
        data = client.recv(4096)
        self.assertEqual(json.loads(data.decode()), {"cmd": "create", "to": "bob", "body": "Account created", "from": "", "error": False})
        # list accounts
        msg = {"cmd": "list", "from": "bob", "to": "","body": "*"}
        client.sendall(json.dumps(msg).encode())
        data = client.recv(4096)
        self.assertEqual(json.loads(data.decode()), {"cmd": "list", "to": "", "body": "alice,bob", "from": "", "error": False})

        client.close()

    def test_login_logoff(self):
        # test login command with valid credentials
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        msg = {"cmd": "login", "from": "bob", "to": "", "body": ""}
        client.sendall(json.dumps(msg).encode())
        data = client.recv(4096)
        self.assertEqual(json.loads(data.decode()), {"cmd": "login", "to": "bob", "body": "Login successful", "from": "", "error": False})

        msg = {"cmd": "logoff", "from": "bob", "to": "", "body": ""}
        client.sendall(json.dumps(msg).encode())
        data = client.recv(4096)
        self.assertEqual(json.loads(data.decode()), {"cmd": "logoff", "to": "", "body": "User logged off", "from": "", "error": False})

        client.close()

    def test_send_and_deliver(self):
        # test send and deliver commands
        client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client1.connect((HOST, PORT))
        client2.connect((HOST, PORT))
        # login alice
        msg = {"cmd": "login", "from": "alice", "to": "", "body": ""}
        client1.sendall(json.dumps(msg).encode())
        data = client1.recv(4096)
        self.assertEqual(json.loads(data.decode()), {"cmd": "login", "to": "alice", "body": "Login successful", "from": "", "error": False})
        # send message from alice to bob
        msg = {"cmd": "send", "from": "alice", "to": "bob", "body": "Hello, Bob!"}
        client1.sendall(json.dumps(msg).encode())
        data = client1.recv(4096)
        self.assertEqual(json.loads(data.decode()), {"cmd": "send", "to": "", "body": "Message sent", "from": "", "error": False})
        # deliver message, at this point we have not yet logged in bob, so he has to manually request for delivery.
        msg = {"cmd": "deliver", "from": "bob", "to": "","body": ""}
        client1.sendall(json.dumps(msg).encode())
        data = client1.recv(4096)
        self.assertEqual(json.loads(data.decode()), {"cmd": "deliver", "to": "", "body": "Hello, Bob!", "from": "alice", "error": False})

        client1.close()
        client2.close()

    def test_delete(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        msg = {"cmd": "delete", "from": "bob", "to": "","body": ""}
        client.sendall(json.dumps(msg).encode())
        data = client.recv(4096)
        self.assertEqual(json.loads(data.decode()), {"cmd": "delete", "to": "", "body": "Account deleted", "from": "", "error": False})

        # now check account list, should only has alice
        msg = {"cmd": "list", "from": "bob", "to": "","body": "*"}
        client.sendall(json.dumps(msg).encode())
        data = client.recv(4096)
        self.assertEqual(json.loads(data.decode()), {"cmd": "list", "to": "", "body": "alice", "from": "", "error": False})

        # try delete again, should not work
        msg = {"cmd": "delete", "from": "bob", "to": "","body": ""}
        client.sendall(json.dumps(msg).encode())
        data = client.recv(4096)
        self.assertEqual(json.loads(data.decode()), {"cmd": "delete", "to": "", "body": "User does not exist", "from": "", "error": True})

        client.close()

    def tearDown(self):
        # stop server and join thread
        self.server.stop()
 
if __name__ == "__main__":
    # mock_socket = mock.Mock()
    test = TestChatServer()
    test.setUp()
    test.test_create_and_list()
    test.test_login_logoff()
    test.test_send_and_deliver()
    test.test_delete()
    test.tearDown()
    print("Passes all cases.")
    os._exit(1)
