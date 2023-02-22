from concurrent import futures

import pytest
import grpc

import chat_pb2 as chat
import chat_pb2_grpc as rpc
import server as s

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

    def test_create_account(self):
        # Create account for Alice
        request = chat.CreateAccount()
        request.username = 'Alice'
        reply = self.conn.SendCreateAccount(request)
        assert reply.message == 'Account created'
        assert reply.error == False

    def test_send_message(self):
        # Create account for Bob
        request = chat.CreateAccount(username='Bob')
        self.conn.SendCreateAccount(request)

        # Send a message
        send_request = chat.Message(username='Bob',
                                    to='Alice', message='Hello, world!')
        reply = self.conn.SendMessage(send_request)
        assert reply.message == 'Message sent'
        assert reply.error == False

    def test_list_accounts(self):
        # Create account for Charlie
        request = chat.CreateAccount(username='Charlie')
        self.conn.SendCreateAccount(request)

        # Check list of accounts
        list_request = chat.ListAccounts(username='Charlie', wildcard='*')
        reply = self.conn.SendListAccounts(list_request)
        assert reply.message == 'Alice, Bob, Charlie'
        assert reply.error == False

    def test_delete_account(self):
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

    def test_login(self):
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
