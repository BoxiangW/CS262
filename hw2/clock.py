import threading
import random
import time
import socket
import queue
import datetime

class VirtualMachine(threading.Thread):
    def __init__(self, name, host, port, clock_rate, vm_list):
        threading.Thread.__init__(self)
        self.name = name
        self.host = host
        self.port = port
        self.clock_rate = clock_rate
        self.message_queue = queue.Queue()
        self.vm_list = vm_list
        self.logical_clock = 0
        self.log = []

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"{self.name}: Listening on {self.host}:{self.port}")
        while True:
            client, address = self.socket.accept()
            data = client.recv(1024).decode()
            if data:
                self.message_queue.put(data)
                # global_clock = datetime.datetime.now()
                # self.logical_clock = max(self.logical_clock, int(data)) + 1
                # self.log.append(f"Received message {data}, Global time: {global_clock}, Message Queue Length: {self.message_queue.qsize()}, Logical Clock: {self.logical_clock}")
            client.close()

    def send_message(self, message, target):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target.host, target.port))
        sock.sendall(str(message).encode())
        sock.close()
        global_clock = datetime.datetime.now()
        self.logical_clock += 1
        self.log.append(f"Sent message {message}, Global time: {global_clock}, Logical Clock: {self.logical_clock}")

    def tick(self):
        if not self.message_queue.empty():
            data = self.message_queue.get()
            global_clock = datetime.datetime.now()
            self.logical_clock = max(self.logical_clock, int(data)) + 1
            self.log.append(f"Received message {data}, Global time: {global_clock}, Message Queue Length: {self.message_queue.qsize()}, Logical Clock: {self.logical_clock}")
        else:
            event = random.randint(1, 10)
            if event == 1:
                target = self.vm_list[event-1]
                self.send_message(self.logical_clock, target)
            elif event == 2:
                target = self.vm_list[event-1]
                self.send_message(self.logical_clock, target)
            elif event == 3:
                for target in self.vm_list:
                    self.send_message(self.logical_clock, target)
            else:
                global_clock = datetime.datetime.now()
                self.logical_clock += 1
                self.log.append(f"Internal event, Global time: {global_clock}, Logical Clock: {self.logical_clock}")
        time.sleep(1 / self.clock_rate)

def main():
    vm1 = VirtualMachine("VM1", "localhost", 8000, random.randint(1, 6), [])
    vm2 = VirtualMachine("VM2", "localhost", 8001, random.randint(1, 6), [])
    vm3 = VirtualMachine("VM3", "localhost", 8002, random.randint(1, 6), [vm1, vm2])
    vm1.vm_list = [vm3, vm2]
    vm2.vm_list = [vm1, vm3]
    vm1.start()
    vm2.start()
    vm3.start()
    while True:
        vm1.tick()
        vm2.tick()
        vm3.tick()

if __name__ == '__main__':
    main()
