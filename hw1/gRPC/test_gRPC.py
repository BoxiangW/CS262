from concurrent import futures

import threading
import grpc

import chat_pb2 as chat
import chat_pb2_grpc as rpc
import server as s
import client as c

PORT = 56789


class TestChatRoom:
    # server side
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=10))
    rpc.add_ChatServerServicer_to_server(
        s.ChatServer(), server)
    server.add_insecure_port('[::]:' + str(PORT))
    server.start()

    # client side
    channel = grpc.insecure_channel('localhost:' + str(PORT))
    conn = rpc.ChatServerStub(channel)

    def _start_stream(self):
        n = chat.Id()
        n.username = 'Bob'
        for note in self.conn.ChatStream(n):
            print("\n[Receive]{}: {}".format(note.username, note.message))

    def test_create_account(self, capsys):
        # Create account for Alice
        request = chat.CreateAccount()
        request.username = 'Alice'
        reply = self.conn.SendCreateAccount(request)
        assert reply.message == 'Account created'
        assert reply.error == False

        # Check server output
        captured = capsys.readouterr()
        assert captured.out == "[Create] Alice\n"

    def test_send_message(self, capsys):
        # Create account for Bob
        request = chat.CreateAccount(username='Bob')
        self.conn.SendCreateAccount(request)

        # Send a message
        send_request = chat.Message(username='Alice',
                                    to='Bob', message='Hello, world!')
        reply = self.conn.SendMessage(send_request)
        assert reply.message == 'Message sent'
        assert reply.error == False

        # Check server output
        captured = capsys.readouterr()
        assert captured.out == "[Create] Bob\n[Message] Alice to Bob: Hello, world!\n"

    def test_list_accounts(self, capsys):
        # Create account for Charlie
        request = chat.CreateAccount(username='Charlie')
        self.conn.SendCreateAccount(request)

        # Check list of accounts
        list_request = chat.ListAccounts(username='Charlie', wildcard='*')
        reply = self.conn.SendListAccounts(list_request)
        assert reply.message == 'Alice, Bob, Charlie'
        assert reply.error == False

        # Check server output
        captured = capsys.readouterr()
        assert captured.out == "[Create] Charlie\n[List] Charlie: *\n[List] *: Alice, Bob, Charlie\n"

    def test_delete_account(self, capsys):
        # Create account for Dave
        request = chat.CreateAccount(username='Dave')
        self.conn.SendCreateAccount(request)

        # Check list of accounts to make sure Dave is there
        list_request = chat.ListAccounts(username='Alice', wildcard='*')
        reply = self.conn.SendListAccounts(list_request)
        assert reply.message == 'Alice, Bob, Charlie, Dave'
        assert reply.error == False

        # Delete account for Dave
        delete_request = chat.DeleteAccount(username='Dave')
        reply = self.conn.SendDeleteAccount(delete_request)
        assert reply.message == 'Account deleted'
        assert reply.error == False

        # Check list of accounts to make sure Dave is gone
        list_request = chat.ListAccounts(username='Alice', wildcard='*')
        reply = self.conn.SendListAccounts(list_request)
        assert reply.message == 'Alice, Bob, Charlie'
        assert reply.error == False

        # Check server output
        captured = capsys.readouterr()
        assert captured.out == "[Create] Dave\n[List] Alice: *\n[List] *: Alice, Bob, Charlie, Dave\n[Delete] Dave\n[List] Alice: *\n[List] *: Alice, Bob, Charlie\n"

    def test_login(self, capsys):
        # Create account for Eve
        request = chat.CreateAccount(username='Eve')
        self.conn.SendCreateAccount(request)

        # Check list of accounts to make sure Eve is there
        list_request = chat.ListAccounts(username='Alice', wildcard='*')
        reply = self.conn.SendListAccounts(list_request)
        assert reply.message == 'Alice, Bob, Charlie, Eve'
        assert reply.error == False

        # Logout account for Eve
        logout_request = chat.Logout(username='Eve')
        reply = self.conn.SendLogout(logout_request)
        assert reply.message == 'Logout successful'
        assert reply.error == False

        # Check list of accounts to make sure Eve is still there
        list_request = chat.ListAccounts(username='Alice', wildcard='*')
        reply = self.conn.SendListAccounts(list_request)
        assert reply.message == 'Alice, Bob, Charlie, Eve'
        assert reply.error == False

        # Login account for Eve
        login_request = chat.Login(username='Eve')
        reply = self.conn.SendLogin(login_request)
        assert reply.message == 'Login successful'
        assert reply.error == False

        # Check list of accounts to make sure Eve is still there
        list_request = chat.ListAccounts(username='Alice', wildcard='*')
        reply = self.conn.SendListAccounts(list_request)
        assert reply.message == 'Alice, Bob, Charlie, Eve'
        assert reply.error == False

        # Check server output
        captured = capsys.readouterr()
        assert captured.out == "[Create] Eve\n[List] Alice: *\n[List] *: Alice, Bob, Charlie, Eve\n[Logout] Eve\n[List] Alice: *\n[List] *: Alice, Bob, Charlie, Eve\n[Login] Eve\n[List] Alice: *\n[List] *: Alice, Bob, Charlie, Eve\n"
