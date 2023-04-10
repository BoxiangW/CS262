# Engineering Notebook

Following is the addition that we’ve added to our chat service to ensure fault tolerance using

**Persistent:**

Main Idea:

We use the pickle module in Python to serialize the sent messages and user account info, and store them in a binary file. This action is done every time the state updates for a server (so these information are changed), and when the server start backup, it first read from the saved binary file to repopulate its fields.

Server: 



1. We define the function persist() that writes self.accounts and self.logout_accounts to a binary file. Self.accounts saves the account information for each user, and self.logout_accounts saves the undelivered message to each user when they are offline.
2. We also define the function readPersist() that read from the binary file and repopulate these fields in order to achieve persistency.

**Replication:**

Main Idea:



1. The main idea for us to achieve replication is to ensure when the main server is down, one of the backup servers can become the main server and have exactly the same state as the main server.
2. In order for us to achieve this, we used the idea of a **master-slave replication**. That is, we have a master server and several slave servers. Each write request to the server (any client requests that requires the change of state for the server, such as new client register, message sent, etc) will require all slave servers to be synchronized on the change for master to perform the change of state.
3. We do this by propagating this request to the slave servers upon receiving the request, only when **all** slave servers confirm this change, then the master server can make this change and confirm with the client.

Protobuf (chat.proto):



1. Added `UpdateMessage` and `SendHeartbeat` to the protobuf file. `UpdateMessage` is used to make sure slave servers have the same list of undelivered message after master deliver them to clients, and `SendHeartbeat` is used for server status transformation.

Server:



1. For intra-server communication, we first store a list of server’s ip address and port for each server (that is, all server know where the other servers are initially).
2. During the startup of a server, it will go through these ips and set up gRPC stub with them and store them in self.stubs, for communications later on.
3. For every write request (create account, send message), when the master server receives the request from the client, it will send the same request to its slave servers, so that the update may be propagated and causing the slave server to receive the request and update their state as well.
4. Doing this will allow replication on the backend, while also not implementing or writing any new code to increase the complexity of our codebase.

Client:



1. Important Assumption: Client always know who’s the master when the client first startup. This means that we can manually connect the client to the master (by manually inputting the IP address and port of the master server).

**Fault-tolerance:**

Main Idea:

Essentially there are two cases that may occur on the server side under our master-slave replication algorithm. 1. The master fails. 2. The server fails. The trickiest part is of course when the master fails, which will requires a reassignment of a new master among all slave servers, and most importantly, the slave servers will need to reach a consensus of who will become the new master. Since we didn’t implement a consensus algorithm such as Paxos or Raft, just by the servers themselves it is impossible to come up with a consensus. Currently, many existing implementations of the master-slave algorithm make use of an administrator node, which is in charge of assigning the new master server, and since there is only one decision maker, there is consensus. However, doing so will allow our system to have a new point of failure, once the administrator node is down, everything will fail.

So how do we maintain consensus among servers while also eliminate the need for single administrator node? Our idea is simple: we offload this task of administrating to the client. The client will now choose who will be the master server. 

All Client will choose the new master based on a simple algorithm, starting from their current server (which is the master server but suddenly losses their connection), they look for the next server with server ID = current server + 1 (If reaches the end, circle back to id 0), until they find the a server who is still online. As soon as a client find such server, they will update the server to let it know that it is now the master.

This algorithm will reach consensus, since every client must be originally connected to the same master server who failed, starting from the same point, they use the same algorithm to find the next one, therefore the next one they found will be the same as well.

On the server side, we do not need to have them communicating with each other for an election to raise the new master, since all of these tasks will be done on the client side.

Server:



1. 