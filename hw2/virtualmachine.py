from multiprocessing import Process
from threading import Thread
import random
import time
import socket
import datetime


class VirtualMachine(Process):
    """Process representing a single virtual machine for hw 2.

    Attributes:
        name: A string indicates the name.
        host: A string indicates the host.
        port: An integer indicates the port.
        clock_rate: An integer indicates the clock rate.
        vm_address_list: A list of tuples containing addresses.
        message_queue: A queue for storing messages.
        logical_clock: An integer indicates the logical clock time.
        log_file: A string indicates the log file name.
    """

    def __init__(self, name, host, port, clock_rate, vm_address_list):
        """Initializes the instance with basic settings.

        Args:
          name: Used to identify the VM.
          host: Used to connect to the VM.
          port: Used to connect to the VM.
          clock_rate: Used to control the speed of the VM.
          vm_address_list: Used to send messages to other VMs.
        """
        Process.__init__(self)
        self.name = name
        self.host = host
        self.port = port
        self.clock_rate = clock_rate
        self.vm_address_list = vm_address_list
        self.sender = []
        self.message_queue = []
        self.logical_clock = 0
        self.log_file = f"{self.name}_log.txt"
        open(self.log_file, 'w')
        self.log(f"=============LOG START=============\n")
        self.log(f"clock_rate = {clock_rate}\n")

    def run(self):
        """Method representing the process's activity.

        Overide the run method of multiprocessing.Process. See details at
        https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process.run
        """
        # start a thread to receive messages
        Thread(target=self.receive_thread).start()

        # wait for all VMs to start otherwise the VMs might not be able to connet
        time.sleep(1)

        # send messages
        Thread(target=self.tick_thread).start()

    def receive_thread(self):
        """Thread for receiving messages."""
        # create an INET, STREAMing socket
        receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receiver.bind((self.host, self.port))
        receiver.listen(2)
        print(f"{self.name}: Listening on {self.host}:{self.port}")

        # accept connections from outside
        while True:
            conn, address = receiver.accept()
            Thread(target=self.receive_message, args=(conn,)).start()

    def receive_message(self, conn):
        """Receive message from other VMs.

        Args:
          conn: Socket connection.
        """
        while True:
            data = conn.recv(1024).decode()
            if data:
                self.message_queue.append(data)

    def tick_thread(self):
        """Thread for ticking the VM."""
        # create a socket for each VM
        for _ in range(len(self.vm_address_list)):
            self.sender.append(socket.socket(
                socket.AF_INET, socket.SOCK_STREAM))

        # connect to other VMs
        try:
            for i in range(len(self.vm_address_list)):
                self.sender[i].connect(
                    (self.vm_address_list[i][0], self.vm_address_list[i][1]))

        except socket.error as e:
            print("Error connecting sender: %s" % e)

        while True:
            starttime = time.time()
            self.tick()  # tick the VM
            endtime = time.time()
            elapsed = endtime - starttime
            time.sleep((1 / self.clock_rate) - elapsed)

    def tick(self):
        """Method representing the VM's activity."""

        # if the message queue is not empty, take one message off the queue and process it
        if len(self.message_queue):
            self.logical_clock = max(
                self.logical_clock, int(self.message_queue[0])) + 1
            data = self.message_queue.pop(0)
            log_message = f"[Receive]: {data}, [System time]: {datetime.datetime.now()}, [Message Queue Length]: {len(self.message_queue)}, [Logical Clock Time]: {self.logical_clock}\n"
            self.log(log_message)

        # if the message queue is empty, send message or do internal event
        else:
            event = random.randint(1, 10)
            self.logical_clock += 1
            if event <= 3:  # send message
                if event == 1:  # send message to one VM
                    self.sender[0].send(str(self.logical_clock).encode())
                elif event == 2:  # send message to the other VM
                    self.sender[1].send(str(self.logical_clock).encode())
                elif event == 3:  # send message to both VM
                    for i in range(len(self.sender)):
                        self.sender[i].send(str(self.logical_clock).encode())
                log_message = f"[Send]: {self.logical_clock}, [System time]: {datetime.datetime.now()}, [Logical Clock Time]: {self.logical_clock}\n"
                self.log(log_message)

            else:  # do internal event
                log_message = f"[Internal event], [System time]: {datetime.datetime.now()}, [Logical Clock Time]: {self.logical_clock}\n"
                self.log(log_message)

    def log(self, message):
        """Logs the message to the log file.

        Args:
          message: String to be logged.
        """
        with open(self.log_file, 'a+') as logfile:
            logfile.write(message)


if __name__ == '__main__':
    # set clock rates for each VM
    vm1_clockrate = random.randint(1, 6)
    vm2_clockrate = random.randint(1, 6)
    vm3_clockrate = random.randint(1, 6)
    print("VM1 clock rate: ", vm1_clockrate)
    print("VM2 clock rate: ", vm2_clockrate)
    print("VM3 clock rate: ", vm3_clockrate)

    vm1_address, vm1_port = "localhost", 10113
    vm2_address, vm2_port = "localhost", 10114
    vm3_address, vm3_port = "localhost", 10115

    # init VMs
    vm1 = VirtualMachine("VM1", "localhost", 10113, vm1_clockrate, [
                         (vm2_address, vm2_port), (vm3_address, vm3_port)])
    vm2 = VirtualMachine("VM2", "localhost", 10114, vm2_clockrate, [
                         (vm3_address, vm3_port), (vm1_address, vm1_port)])
    vm3 = VirtualMachine("VM3", "localhost", 10115, vm3_clockrate, [
                         (vm1_address, vm1_port), (vm2_address, vm2_port)])

    vm1.start()
    vm2.start()
    vm3.start()

    time.sleep(60)  # run for 1 minutes

    # wait for processes to finish
    vm1.terminate()
    vm2.terminate()
    vm3.terminate()
