# Fault-tolerant chat service using gRPC
This is a fault-tolerant chat service using gRPC. This service is able to run on multiple servers in a distributed network environment, and the messages are synchronized between all the servers.

## Installation
To run this service, you need Python 3.x and grpcio and protobuf libraries.

`pip install grpcio protobuf`
Clone the repository and run the server with the following command:

`python server.py [server_id] [restart]`
server_id: Integer to identify each server. Should be different for each server.
restart: If set to True, the server will try to restore its previous state from a binary file.

## Usage
The following are the functionalities provided by the chat service:

SendMessage: Sends a message to a specific user. The server will synchronize the message with other servers.
SendCreateAccount: Creates a new account for a user. The server will synchronize the account creation with other servers.
SendListAccounts: Returns a list of accounts matching a specified wildcard pattern.
SendDeliverMessages: Delivers all the messages received while the user was logged out.
Server Architecture
The chat service consists of multiple servers running the same code, connected through gRPC. The servers synchronize messages with each other by calling each other's functions.

## Persistence
The chat service can save its current state to a binary file at any time. When a server is restarted, it can try to restore its previous state from the binary file. The binary files are named log_[server_id].bin.