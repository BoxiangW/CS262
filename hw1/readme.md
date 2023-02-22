
## Simple Chat App

This is a simple chat application that allows users to send and receive messages over a network. The application is written in Python, the custom version uses sockets and JSON for communication, and the gRPC version uses gRPC for communication.

  

### Requirements

-   Python 3.6 or higher

-   gRPC 1.37.0 or higher

-   Socket

  

### Installation

1. Install Python 3.x
2. Clone this repository

**To run gRPC version**
3.  Install gRPC: `pip install grpcio grpcio-tools`
4.  Generate the required Python code from the .proto files:

`python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto
`


### Usage

Open two terminals or command prompt windows.

In one window, navigate to the directory where the code is cloned and run `python server.py`.

In the other window, navigate to the same directory and run `python client.py`.

The client will prompt you to enter the host IP address.

Once the connection is established, you can follow the prompts to create a new account, login, send messages, and perform other actions.

### Functions

Login: Log in to the chat app with a username.

Create an account: Create a new account with a specified username.

Send a message: Send a message to another user in the chat app.

Deliver undelivered messages: Get all messages that have not been delivered.

List accounts: List all registered usernames.

Delete an account: Delete your own account.

Log off: Log off from the chat app.

  

### How it works

**Custom version**
The server waits for incoming connections and handles incoming messages from clients. The server maintains a list of all the users that are currently logged in, and it handles incoming messages by sending them to the intended recipient.

The client creates a socket and connects to the server. Once the connection is established, the client sends JSON-encoded messages to the server to perform various actions, such as creating an account, logging in, and sending messages.

**gPRC version**
This program uses gRPC, a high-performance, open-source universal RPC framework, to implement a simple chat server and client. The server is responsible for managing accounts and storing messages, while the client allows users to create accounts, log in, send and receive messages, and perform other related operations.

When the client starts, it creates a gRPC channel and connects to the server. The client then enters a main loop, where it prompts the user to choose an operation: create an account, log in, or exit. If the user chooses to create an account, the client sends a request to the server to create a new account with the specified username. If the user chooses to log in, the client sends a request to the server to log in with the specified username. In either case, if the request is successful, the client creates a new thread to listen for new messages from the server.

Once the user is logged in, the client enters a second loop, where it prompts the user to choose an operation: send a message, deliver undelivered messages, list accounts, delete an account (and log out), or log out. If the user chooses to send a message, the client prompts the user for the recipient's username and the message content, then sends a request to the server to send the message. If the user chooses to deliver undelivered messages, the client sends a request to the server to deliver all messages that have not yet been delivered to the user. If the user chooses to list accounts, the client sends a request to the server to list all accounts matching a specified wildcard pattern. If the user chooses to delete an account, the client sends a request to the server to delete the account and log out. If the user chooses to log out, the client sends a request to the server to log out and exits the program.

The server, on the other hand, listens for requests from clients and responds accordingly. When a client requests to create a new account, the server checks if the account already exists and creates the account if it does not. When a client requests to log in, the server checks if the account exists and logs in the user if it does. When a client requests to send a message, the server adds the message to the recipient's message queue. When a client requests to deliver undelivered messages, the server sends all undelivered messages to the user. When a client requests to list accounts, the server lists all accounts matching the specified wildcard pattern. When a client requests to delete an account, the server deletes the account and logs out the user. When a client requests to log out, the server logs out the user.

## References

-   [gRPC Documentation](https://grpc.io/docs/)