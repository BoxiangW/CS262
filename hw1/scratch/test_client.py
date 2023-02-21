import unittest
import socket
from unittest import mock
from unittest.mock import MagicMock, patch
from client import ChatClient


class TestChatClient(unittest.TestCase):
    # def setUp(self):
    #     self.client = ChatClient("localhost", 56789)

    def test_init(self):
        with mock.patch('socket.socket'):
            client = ChatClient("localhost", 56789)
            self.assertEqual(client.server_host, "localhost")
            self.assertEqual(client.server_port, 56789)
            self.assertEqual(client.sock, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            client.sock.connect.assert_called_once_with(("localhost", 56789))

    def test_login(self):
        with mock.patch('socket.socket'):
            client = ChatClient("localhost", 56789)
            client.login("alice", "password")
            client.sock.sendall.assert_called_once_with(b'{"cmd": "login", "from": "alice", "to": "", "body": "password"}')

    def test_send_message(self):
        with mock.patch('socket.socket'):
            client = ChatClient("localhost", 56789)
            client.username = "alice"
            client.send_message("bob", "hello")
            client.sock.sendall.assert_called_once_with(b'{"cmd": "send", "from": "alice", "to": "bob", "body": "hello"}')

    def test_list_accounts(self):
        with mock.patch('socket.socket'):
            client = ChatClient("localhost", 56789)
            client.username = "alice"
            client.list_accounts("b*")
            client.sock.sendall.assert_called_once_with(b'{"cmd": "list", "from": "alice", "to": "", "body": "b*"}')

    def test_create_account(self):
        with mock.patch('socket.socket'):
            client = ChatClient("localhost", 56789)
            client.create_account("alice", "password")
            client.sock.sendall.assert_called_once_with(b'{"cmd": "create", "from": "alice", "to": "", "body": "password"}')

    def test_delete_account(self):
        with mock.patch('socket.socket'):
            client = ChatClient("localhost", 56789)
            client.username = "alice"
            client.delete_account()
            client.sock.sendall.assert_called_once_with(b'{"cmd": "delete", "from": "alice", "to": "", "body": ""}')

    def test_receive_messages(self):
        with mock.patch('socket.socket'):
            client = ChatClient("localhost", 56789)
            client.username = "alice"
            client.receive_messages()
            client.sock.sendall.assert_called_once_with(b'{"cmd": "deliver", "from": "alice", "to": "", "body": ""}')

    def test_close(self):
        with mock.patch('socket.socket'):
            client = ChatClient("localhost", 56789)
            client.username = "alice"
            client.close()
            client.sock.sendall.assert_called_once_with(b'{"cmd": "close", "from": "alice", "to": "", "body": ""}')
            client.sock.close.assert_called_once()

# if __name__ == "__main__":
#     # mock_socket = mock.Mock()
#     test = TestChatClient()
#     # test.setUp()
#     test.test_init()
#     test.test_login()
#     test.test_send_message()
#     test.test_list_accounts()
#     test.test_create_account()
#     test.test_delete_account()
#     test.test_receive_messages()
#     test.test_close()
