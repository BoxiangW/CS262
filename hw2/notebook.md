# Engineering Notebook

## Decisions

1. We first decided to open and close the socket for every message, but we quickly realized that this is very inefficient becuase opening a socket requires 3 packet exchanges, and closing it requires 4. Therefore we decided to keep the socket open.

2. We defined the VirtualMachine class as a thread as the beginning, but we realized that to make the VM perform send and receive at the same time, we need to make the VM a process. Therefore we changed the VM to a process.

3. We planned to use different threads for sending messages and do internal events, but we realized that with this setting it might be difficult to synchronize the two threads. Therefore we decided to use a single thread for both sending messages and doing internal events, as named as tick.

## Structure

- `VirtualMachine`:

    A Class inherited from Process. It uses two threads to continusly receive messages and tick. It stores multiply sockets for different clients.

  - `__init__(self, name, host, port, clock_rate, vm_address_list)`:

    Initialize the VM. It opens a log file in overwrite mode.

  - `run(self)`:

    The main function of the VM. It creates two threads, one for receiving messages with `target=self.receive_thread` and one for ticking with `target=self.tick_thread`. It overide the run method of multiprocessing.Process. See details at [here](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process.run).

  - `receive_thread(self)`:

    Create a socket and listen to the port. After accepting a connection, it will create a new thread with `target = self.receive_message` to handle the connection.

  - `receive_message(self, conn)`:
  
    After a connection is established, it will receive the message and put it into the message queue.

  - `tick_thread(self)`:

    Create two sockets for sending messages to two other VMs. It will tick every 1/clock_rate seconds. After ticking, it will call `tick()` to operate.

  - `tick(self)`:

    It will check the message queue and do the corresponding operations. If the message queue is not empty, take one message off the queue and process it. If the message queue is empty, generate a random number from 1 to 10. For number 1, send its local logical clock time to one VM. For number 2, send its local logical clock time to the other VM. For number 3, send its local logical clock time to both VMs. Otherwise, do nothing. For all the above, log its operation, system time, and local logical clock time, if message queue is not empty, also log the message queue length.
  
  - `log(self, message)`:

    Helper to log the message to the log file.

## Findings

### Original Settings

For machines that have smaller clock rates, as the time goes by, it will take most of its time receiving meddages. Therefore, it will not be able to send messages to other VMs. This is because the VMs are not synchronized.

**Size of Jumps**:

For machines that has relatively larger clock rates, they will have smaller possibility to have logical clock time jumps and their gap will be smaller. For machines that has relatively smaller clock rates, they will have greater possibility to have logical clock time jumps and their gap will be larger.

**Drifts**:

Smaller clock rates will cause larger drifts because it is more likely to have logical clock time jumps and the gap is larger.

**Length of message queue**:

Smaller clock rates will have longer message queue because it has less chance to send messages to other VMs and it will take more time to deal with the messages in the queue.


### Smaller variation in the clock cycles and a smaller probability of the event being internal

In this case, smaller clock rates will have even greater possibility to have logical clock time jumps and their gap will be even larger, and their message queue will be even longer. Vice versa for larger clock rates.

We found that a machine with relatively samller clock rate has an continusly increasing message queue till the end of the simulation. 