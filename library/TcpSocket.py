"""A simple tcp class that permits to send and receive data
"""
import socket

BUFFER_SIZE = 4096

class TcpSocket:
    
    def __init__(self) -> None:
        self.com_socket: socket.socket = None
        self.address = None

    def wait_connection(self, port: int) -> None:
        self.serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_socket.bind((socket.INADDR_ANY, port))
        self.serv_socket.listen(1)
        self.com_socket, self.address = self.serv_socket.accept()

    def connect(self, ip_address: str, port: int) -> None:
        self.com_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.com_socket.connect((ip_address, port))

    def receive(self) -> str:
        msg_bytes, address = self.com_socket.recvfrom(BUFFER_SIZE)
        message = msg_bytes.decode("utf-8")
        return message

    def receive_bytes(self, num_bytes: int) -> bytes:
        print(f"Receive {num_bytes} bytes")
        data = bytearray()
        while len(data) < num_bytes:
            msg_bytes = self.com_socket.recv(BUFFER_SIZE)
            data.extend(msg_bytes)
        return data

    def send(self, message: str) -> None:
        self.com_socket.send(message.encode("utf-8"))

    def send_bytes(self, data: bytes) -> None:
        self.com_socket.send(data)
