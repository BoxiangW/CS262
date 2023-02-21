import socket
import json
import fnmatch
import threading

# define host and port for server
HOST = 'localhost'
PORT = 56789

# define the maximum message size
MSGLEN = 4096

# create a dictionary to store user accounts and their undelivered messages
users = {}
user_info = {}

# json encoded message: {"cmd": ..., "from": .., "to": ..., "body": ..., "err": ...}

# a message generator function


def create_msg(cmd, src="", to="", body="", err=False):
    msg = {
        "cmd": cmd,
        "from": src,
        "to": to,
        "body": body,
        "error": err
    }
    return json.dumps(msg).encode()

# a message receiver, according to <https://docs.python.org/3/howto/sockets.html>


def receive(conn):
    return conn.recv(MSGLEN)

# a function to handle client connections


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        # receive message from client
        msg = receive(conn).decode()

        # check if message is empty or the client has disconnected
        if not msg:
            print(f"[DISCONNECT] {addr} disconnected.")
            break

        # parse message
        parts = json.loads(msg)
        cmd = parts["cmd"]
        username = parts["from"]

        # handle log in command
        if cmd == "login":
            if (username not in user_info) or (user_info[username] != parts["body"]):
                conn.send(create_msg(
                    cmd, body="Username/Password error", err=True))
            else:
                conn.send(create_msg(cmd, body="Login successful", to=username))

        # handle create account command
        elif cmd == "create":
            # check if username already exists
            if username in users:
                conn.send(create_msg(
                    cmd, body="Username already exists", err=True))
            else:
                # create new user account
                user_info[username] = parts["body"]
                # create the message queue
                users[username] = []
                conn.send(create_msg(cmd, body="Account created", to=username))

        # handle list accounts command
        elif cmd == "list":
            # create a list of usernames matching the wildcard (if any)
            wildcard = parts["body"] if parts["body"] else '*'
            matching_users = fnmatch.filter(list(users.keys()), wildcard)
            # send list of usernames to client
            matching_users = ",".join(matching_users)
            conn.send(create_msg(cmd, body=matching_users))

        # handle send message command
        elif cmd == "send":
            recipient = parts["to"]
            message = parts["body"]
            # check if recipient is a registered user
            if recipient not in users:
                conn.send(create_msg(cmd, body="Recipient not found", err=True))
            else:
                # add message to recipient's message queue
                users[recipient].append((username, message))
                # notify client that message was sent
                conn.send(create_msg(cmd, body="Message sent"))

        # handle deliver messages command
        elif cmd == "deliver":
            if username not in users:
                conn.send(create_msg(cmd, body="User not found", err=True))
            else:
                # retrieve undelivered messages for this user
                messages = users.get(username, [])
                # send messages to client
                for (sender, message) in messages:
                    conn.send(create_msg(cmd, src=sender, body=message))
                # clear user's message queue
                users[username] = []

        # handle delete account command
        elif cmd == "delete":
            # check if user has undelivered messages
            if username not in users:
                conn.send(create_msg(cmd, body="User does not exist", err=True))
            elif username in users and len(users[username]) > 0:
                conn.send(create_msg(
                    cmd, body="Undelivered messages exist", err=True))
            else:
                # delete user account
                del users[username]
                del user_info[username]
                # notify client that account was deleted
                conn.send(create_msg(cmd, body="Account deleted"))
                # disconnect client
                # conn.send(create_msg("error", body="disconnect"))
        elif cmd == "close":
            print(f"[DISCONNECT] {addr} disconnected.")
            break

    conn.close()


# create server socket and start listening for client connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

while True:
    # accept client connection
    conn, addr = server.accept()

    # start a new thread to handle the connection
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
