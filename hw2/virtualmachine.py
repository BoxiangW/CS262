import multiprocessing
import random
import time
import socket
import datetime


class VirtualMachine(multiprocessing.Process):
    """Virtual machine for hw 2.

    Attributes:
        name: A string indicates the name.
        host: A string indicates the host.
        port: An integer indicates the port.
        message_queue: A queue for storing messages.
        vm_list: A list of VirtualMachine instances.
        logical_clock: An integer indicates the logical clock time.
        log_file: A string indicates the log file name.
        receiver: A socket instance for receiving messages.
    """

    def __init__(self, name, host, port, vm_list):
        """Initializes the instance with basic settings.

        Args:
          name: Used to identify the VM.
          host: Used to connect to the VM.
          port: Used to connect to the VM.
          vm_list: Used to send messages to other VMs.
        """
        multiprocessing.Process.__init__(self)
        self.name = name
        self.host = host
        self.port = port
        self.message_queue = []
        self.vm_list = vm_list
        self.logical_clock = 0
        self.log_file = f"{self.name}_log.txt"
        open(self.log_file, 'w')
        self.log(f"=============LOG START=============\n")

    # def __del__(self):
    #     """Delete current instance."""
    #     self.log_file.close()

    def log(self, message):
        """Logs the message to the log file.

        Args:
          message: String to be logged.
        """
        with open(self.log_file, 'a+') as logfile:
            logfile.write(message)

    def run(self):
        """Method representing the process's activity.

        Overide the run method of multiprocessing.Process. See details at
        https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process.run
        """
        # create an INET, STREAMing socket
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver.bind((self.host, self.port))
        self.receiver.listen(5)
        print(f"{self.name}: Listening on {self.host}:{self.port}")

        # accept connections from outside
        while True:
            client, address = self.receiver.accept()
            data = client.recv(1024).decode()
            if data:
                self.message_queue.append(data)
            client.close()

    def send_message(self, target):
        """Send local logical clock time to the target VM.

        Args:
          target: VirtualMachine instance to send the message to.
        """
        # create an INET, STREAMing socket
        sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender.connect((target.host, target.port))
        sender.sendall(str(self.logical_clock).encode())
        sender.close()

    def tick(self):
        """Method representing the VM's activity."""

        # if the message queue is not empty take one message off the queue and process it
        if len(self.message_queue):
            data = self.message_queue.pop(0)
            # update logical clock
            # self.logical_clock = max(self.logical_clock, int(data)) + 1
            self.logical_clock += 1
            log_message = f"[Receive]: {data}, [System time]: {datetime.datetime.now()}, [Message Queue Length]: {len(self.message_queue)}, [Logical Clock Time]: {self.logical_clock}\n"
            self.log(log_message)

        else:  # if the message queue is empty, send message or do internal event
            event = random.randint(1, 10)
            self.logical_clock += 1

            if event <= 3:  # send message
                if event == 1:  # send message to one VM
                    target = self.vm_list[0]
                    self.send_message(target)
                elif event == 2:  # send message to the other VM
                    target = self.vm_list[1]
                    self.send_message(target)
                elif event == 3:  # send message to both VM
                    for target in self.vm_list:
                        self.send_message(target)
                log_message = f"[Send]: {self.logical_clock}, [System time]: {datetime.datetime.now()}, [Logical Clock Time]: {self.logical_clock}\n"
                self.log(log_message)

            else:  # do internal event
                log_message = f"[Internal event], [System time]: {datetime.datetime.now()}, [Logical Clock Time]: {self.logical_clock}\n"
                self.log(log_message)


def handle_tick(vm, clockrate):
    """VM tick handler for threading.

    Args:
        vm: VirtualMachine instance to be ticked.
        clockrate: clock rate of the VM.
    """
    while True:
        vm.tick()  # tick the VM
        time.sleep(1 / clockrate)  # sleep for 1/clockrate seconds


if __name__ == '__main__':

    # init VMs
    vm1 = VirtualMachine("VM1", "localhost", 8000, [])
    vm2 = VirtualMachine("VM2", "localhost", 8001, [])
    vm3 = VirtualMachine("VM3", "localhost", 8002, [])
    vm1.vm_list = [vm2, vm3]
    vm2.vm_list = [vm1, vm3]
    vm3.vm_list = [vm1, vm2]
    vm1.start()
    vm2.start()
    vm3.start()

    # set clock rates for each VM
    vm1_clockrate = random.randint(1, 6)
    vm2_clockrate = random.randint(1, 6)
    vm3_clockrate = random.randint(1, 6)
    print("VM1 clock rate: ", vm1_clockrate)
    print("VM2 clock rate: ", vm2_clockrate)
    print("VM3 clock rate: ", vm3_clockrate)

    # start processes
    multiprocessing.Process(
        target=handle_tick, args=(vm1, vm1_clockrate)).start()
    multiprocessing.Process(
        target=handle_tick, args=(vm2, vm2_clockrate)).start()
    multiprocessing.Process(
        target=handle_tick, args=(vm3, vm3_clockrate)).start()
