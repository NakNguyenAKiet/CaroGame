import socket
import pickle
from game import Game
import struct

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.7"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            # print("Player :",self.client.recv(2048).decode())
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048*2))
            if not received_object:
                pass
            else:
                # Xác định loại đối tượng nhận được và xử lý tương ứng
                if isinstance(received_object, str):
                    pass
                elif isinstance(received_object, Game):
                    return pickle.loads(self.client.recv(2048*2))
                # elif isinstance(received_object, Message):
                #     print(f"Received message from {received_object.sender}: {received_object.message}")
        except socket.error as e:
            print("socket error ",e)