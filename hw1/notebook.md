
## Engineering Notebook:

**Custom wire protocols**:

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
    

This format is consistent whether it is from user to client, or the other way around.

“From” specifies the user who send this message.

“To” specifies the user who is going to receive this message.

“Body” contains the message body, For error message it just says what the error is, for list command it can be the list of account names, etc.

“Err” is a boolean indicating whether a message is an error message, this is important since there are a lot of error message and we want to print them to stderr. Therefore it’s important to group them into their own category.

  

Note that every message between client to server follows this exact same format, we found that every commands use a subset of the 5 fields (“cmd”, “from”, “to”, ”body”, “err”), so this format is adequate for message transmission.

  

**Account Creation/Deletion:**

We use a dictionary to store the account info, mapping username to password.

We use another dictionary to store undelivered messages, mapping username to a message queue.

We choose this because dictionary gives us a constant lookup time, allowing us to quickly check whether a user exist, which is crucial for message delivery error checking and account creation/deletion.

  

At first we only have 1 dictionary, which maps username to a message queue. Which we thought is enough for account creation/deletion (check for dictionary keys) and sending messages. However we quickly realized that user cannot log in again after quitting, therefore we need some kind of authentication and a log in system.

  

**Message Sending**:

Every message send from one user to another, is stored in the receiving user’s message queue automatically. Only when that user request delivering using the “deliver” command, the server will then release all unsend message in the queue to user. This satisfy the requirement that all message is delivered upon request.

  

To achieve the requirement that “message are sent to logged-in users automatically, and store in the message queue for offline users”, on the client side, we have a function that call the deliver function every second. By doing this, users that are logged in can automatically receive new messages, while offline user won’t be able to call this function therefore all undelivered messages are stored in their message queue, We also ensure that there’s only one way to receive message which avoids any confusion that may arise.

  

**Server Setup:**

The single server binds to an address and port, and listen for any incoming connections. For any new connection, we create a new thread to handle that user.

  

**Client Setup:**

The client has three threads, 1 thread acts as the user interface that prompt user for actions, and send requests according to user’s input. Another thread is in charge of receiving the messages, in an infinite loop, it will wait for messages and print them accordingly based on the message content. The last thread is in charge of sending automatic requests to the server to deliver unsent messages, every second. By doing this we separates input/output or send/receive to different threads, avoiding any confusion