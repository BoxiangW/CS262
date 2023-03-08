
# Virtual Machine with Clock
The code provided is an implementation of a distributed system where multiple virtual machines (VMs) are running simultaneously. The `VirtualMachine` class represents each of these VMs and they communicate with each other by exchanging messages. The code uses both threads and processes to achieve concurrency.

The `VirtualMachine` class has the following attributes:

-   `name`: A string that identifies the VM.
-   `host`: A string that represents the host address of the VM.
-   `port`: An integer that represents the port number of the VM.
-   `clock_rate`: An integer that represents the clock rate of the VM.
-   `vm_address_list`: A list of tuples that contains the addresses of other VMs in the system.
-   `message_queue`: A list that stores messages received by the VM.
-   `logical_clock`: An integer that represents the logical clock time of the VM.
-   `log_file`: A string that represents the file name of the log file for the VM.

The `VirtualMachine` class has the following methods:

-   `__init__(self, name, host, port, clock_rate, vm_address_list)`: Initializes the `VirtualMachine` object with the given parameters. It also initializes the `message_queue`, `logical_clock`, and `log_file` attributes.
-   `run(self)`: This is the main method of the `VirtualMachine` object that is executed when the VM is started. It starts a thread to receive messages and sends messages to other VMs. It waits for all VMs to start before starting to send messages.
-   `receive_thread(self)`: This is a thread that listens for messages from other VMs.
-   `receive_message(self, conn)`: This method is called by the `receive_thread` to receive messages from other VMs.
-   `tick_thread(self)`: This is a thread that is used to tick the VM. It sends messages or performs internal events.
-   `tick(self)`: This method is called by the `tick_thread` to perform the VM's activity. It processes messages if any, sends messages or performs internal events.
-   `log(self, message)`: This method is used to log messages to the log file.

### Installation

1.  Clone the repository to your local machine using `git clone <repo link>`
2.  Navigate to the cloned directory `cd <directory name>`

### Usage

To run the program, simply execute the `virtualmachine.py` file with Python 3.x. The code will execute on a single machine with 3 processes, each representing a virtual machine.

`python virtualmachine.py` 

The program will output the logs for each virtual machine to separate files in the format `VMx_log.txt`, where `x` is the virtual machine number.