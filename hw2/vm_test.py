import unittest
from multiprocessing import Manager
from virtualmachine import VirtualMachine
from threading import Thread
import time
import random
import socket


class TestVirtualMachine(unittest.TestCase):

    def setUp(self):
        manager = Manager()
        vm1_clockrate = random.randint(1, 6)
        vm2_clockrate = random.randint(1, 6)
        vm1_address, vm1_port = "localhost", 10119
        vm2_address, vm2_port = "localhost", 10118

        self.msg_queues = [manager.list() for _ in range(2)]
        self.vms = [
            VirtualMachine("VM1", "localhost", 10119, vm1_clockrate, [
                         (vm2_address, vm2_port)]),
            VirtualMachine("VM2", "localhost", 10118, vm2_clockrate, [
                         (vm1_address, vm1_port)])
        ]
        self.vms[0].message_queue = self.msg_queues[0]
        self.vms[1].message_queue = self.msg_queues[1]

        self.t = Thread(target=self.vms[1].receive_thread)
        self.t.start()

    def test_virtual_machine(self):
        vm = self.vms[0]
        for _ in range(len(vm.vm_address_list)):
            vm.sender.append(socket.socket(
                socket.AF_INET, socket.SOCK_STREAM))

        for i in range(len(vm.vm_address_list)):
            vm.sender[i].connect(
                (vm.vm_address_list[i][0], vm.vm_address_list[i][1]))


        # Test Send Msg
        for _ in range(5):
            self.vms[0].sender[0].send(b'test message')
            self.vms[0].message_queue.append('test message')
            time.sleep(1)

        # Wait for messages to be processed
        time.sleep(1)

        # Check if both VMs received the same messages
        self.assertEqual(len(self.msg_queues[0]), len(self.msg_queues[1]))
        for i in range(len(self.msg_queues[0])):
            self.assertEqual(self.msg_queues[0][i], self.msg_queues[1][i])


        # Test Log
        self.vms[0].log_file = 'unittest.txt'
        self.vms[0].log("Unit Test Message 1")

        with open('unittest.txt') as f:
            first_line = f.readline()
            self.assertEqual(first_line, "Unit Test Message 1")
