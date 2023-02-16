import socket
import json
import fnmatch
import threading

# define host and port for server
HOST = 'localhost'
PORT = 55555

# create a dictionary to store user accounts and their undelivered messages
users = {}

# json encoded message: {"cmd": ..., "from": .., "to": ..., "body": ...}

# define a function to handle client connections
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        # receive message from client
        msg = conn.recv(1024).decode("utf-8")

        # check if message is empty or the client has disconnected
        if not msg or msg == "disconnect":
            print(f"[DISCONNECT] {addr} disconnected.")
            break

        # parse message
        parts = json.loads(msg)
        cmd = parts["cmd"]
        username = parts["from"]

        # handle create account command
        if cmd == "create":
            # check if username already exists
            if username in users:
                conn.send("error|Username already exists".encode())
            else:
                # create new user account
                users[username] = []
                conn.send("success|Account created".encode())

        # handle list accounts command
        elif cmd == "list":
            # create a list of usernames matching the wildcard (if any)
            wildcard = parts["body"] if len(parts) > 3 else ""
            matching_users = fnmatch.filter(list(users.keys()), wildcard)
            # send list of usernames to client
            conn.send("list|" + ",".join(matching_users).encode())

        # handle send message command
        elif cmd == "send":
            recipient = parts["to"]
            message = parts["body"]
            # check if recipient is a registered user
            if recipient not in users:
                conn.send("error|Recipient not found".encode())
            else:
                # add message to recipient's message queue
                users[recipient].append((username, message))
                # notify client that message was sent
                conn.send("success|Message sent".encode())

        # handle deliver messages command
        elif cmd == "deliver":
            # retrieve undelivered messages for this user
            messages = users.get(username, [])
            # send messages to client
            for (sender, message) in messages:
                conn.send(f"message|{sender}|{message}".encode())
            # clear user's message queue
            users[username] = []

        # handle delete account command
        elif cmd == "delete":
            # check if user has undelivered messages
            if username in users and len(users[username]) > 0:
                conn.send("error|Undelivered messages exist".encode())
            else:
                # delete user account
                if username in users:
                    del users[username]
                # notify client that account was deleted
                conn.send("success|Account deleted".encode())
                # disconnect client
                conn.send("disconnect".encode())
                conn.close()
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

