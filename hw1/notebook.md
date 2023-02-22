
# Engineering Notebook

## Custom wire protocols:

At the initial stage, we are thinking of using simply a string to encode everything, but we quickly realized that it’s very hard to format it so that we can encoder/decode it easily. For example, if there’s a message from user A to user B containing the body “Hello”, and we format it in string format as “A|B|Hello”, then we can decode it using the “|” as the split separator, however if the message body also include |, then the separator will not work.


Eventually we decided to use JSON, and encode it into binary format for the transmission of data between server and client. Reasons are:

  

1.  Human-readable format: JSON is a lightweight data interchange format that is easy for humans to read and write, making it easy to understand and debug.
    
2.  Wide support: JSON is supported by a wide range of programming languages, making it an ideal choice for interoperability between different systems.
    
3.  Efficient parsing: JSON has a simple syntax that can be parsed quickly and efficiently, making it ideal for use in high-performance applications.
    
4.  Compact size: JSON is a relatively compact format, meaning that it requires less bandwidth to transmit data, which can be particularly important for mobile applications and low-bandwidth networks.
    
5.  Ease of use: JSON is easy to use and requires minimal setup, making it a popular choice for web APIs and other data exchange scenarios.
    

  

For every message between client and server, we format it this way:

{"cmd": ..., "from": .., "to": ..., "body": ..., "err": ...}

“Cmd” specifies which command it is:

1.  Create: create an account
    
2.  Delete: delete an account
    
3.  Send: sending an message to another user
    
4.  Deliver: requesting undelivered message to be delivered
    
5.  List: list all accounts matching the wildcard given.
    
6.  Close: telling the server a client closed their connection.

7.  Login: log in a specific user

8.  Logoff: telling the server a client has logged off, therefore we should remove it from active_users.
    

This format is consistent whether it is from user to client, or the other way around.

“From” specifies the user who send this message.

“To” specifies the user who is going to receive this message.

“Body” contains the message body, For error message it just says what the error is, for list command it can be the list of account names, etc.

“Err” is a boolean indicating whether a message is an error message, this is important since there are a lot of error message and we want to print them to stderr. Therefore it’s important to group them into their own category.

  

Note that every message between client to server follows this exact same format, we found that every commands use a subset of the 5 fields (“cmd”, “from”, “to”, ”body”, “err”), so this format is adequate for message transmission.

  

**Account Creation/Deletion:**

We use a dictionary to store undelivered messages, mapping username to a message queue.

We use another dictionary to store active users and their connection, so that we can quickly identify whether a message recipient is logged-in and send them their message.

We choose this because dictionary gives us a constant lookup time, allowing us to quickly check whether a user exist, which is crucial for message delivery error checking and account creation/deletion.


At first we only have 1 dictionary, which maps username to a message queue. Which we thought is enough for account creation/deletion (check for dictionary keys) and sending messages. However we quickly realized that user cannot log in again after quitting, therefore we need some kind of authentication and a log in system.

We also didn't track the user's logged-in status initially, but we soon realized that we are unable to track which user is active before sending them the message.

  

**Message Sending**:

There are two ways messages are being delivered. For a recipient who is logged in, we directly send the message to them.

For a recipient who is logged off, we store the message in their corresponding message queue. Only when that user request delivering using the “deliver” command, the server will then release all unsend message in the queue to user. This satisfy the requirement that all undelivered message is delivered upon request.

  

**Server Setup:**

The single server binds to an address and port, and listen for any incoming connections. For any new connection, we create a new thread to handle that user.

  

**Client Setup:**

The client has three threads, 1 thread acts as the user interface that prompt user for actions, and send requests according to user’s input. Another thread is in charge of receiving the messages, in an infinite loop, it will wait for messages and print them accordingly based on the message content. The last thread is in charge of sending automatic requests to the server to deliver unsent messages, every second. By doing this we separates input/output or send/receive to different threads, avoiding any confusion.


## gRPC version:

We use gRPC to implement the chat room server as well. Both server part and client part are implemented in Python. The server and client communicate with each other using gRPC. The server is implemented in the file server.py, and the client is implemented in the file client.py. Protobuf is used to define the message format.

**Procedure for user**:

1. Start the server by running the command `python server.py`
2. Start the client by running the command `python client.py`
3. Client part will ask for server address which is `localhost` by default, we set the port to be 56789.
4. User enter a loop with 3 options: create account, login, or quit.
    - Create account: user enter a username, client will check its not empty, and the server will create an account with that username. If the username already exists, the server will return an error message.
    - Login: user enter a username, client will check its not empty, and the server will check if the username exists. If the username does not exist, the server will return an error message. If the username is already logged in, the server will return an error message. Else the server will return a success message and the user enter a second loop.
    - quit: user quit the program.
5. In the second loop, user have 5 options: send message, deliver undelivered message, list accounts, delete account, or logout.
    - Send message: user enter a username and a message, client side will check they are not empty, and the server side will check if the username exists. If the username does not exist, the server will return an error message. Else the server will return a success message and send the message to the user or store the message for users not online.
    - Deliver undelivered message: the server will send all undelivered message to the user.
    - List accounts: user enter an optional wildcard, and the server will return a list of accounts matching the wildcard.
    - Delete account: the server will check if the user has undelivered messages. If there is undelivered messages, the server will return an error message. Else the server will return a success message and delete the account quit the program.
    - logout: the server will return a success message and quit the program.


**Server side implementation**:

Use a dict to store the username, online status and the corresponding message queue. The key is the username, and the value is the status and the message queue. `accounts = {username: [status, message queue]}` Message queue is a list of messages in the type of gRPC. The status is a boolean value, True means the user is online, False means the user is offline.

With response-streaming gRPC, serer will continue pop the message queue and send the message to the user until the queue is empty. If the user is offline, the server will use another dict to store undelivered message. After the delivery option, the server will push the undelivered message queue to dict `account` and thus receive them.


## Comparison:

Advantages of gRPC:
- Easy to use, we can use different languages for client and server.
- `.proto` file is easy to understand and modify.