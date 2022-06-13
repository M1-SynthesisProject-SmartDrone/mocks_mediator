"""A simple udp class that permits to send and receive data
"""
import socket
from loguru import logger
from typing import Any, Tuple

BUFFER_SIZE = 65535

class UdpSocket:
    
    def __init__(self, port: int) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", port))
        self.address = None

    def receive(self) -> str:
        msg_bytes, address = self.sock.recvfrom(BUFFER_SIZE)
        message = msg_bytes.decode("utf-8")
        logger.debug(f"Received from {address}: {message}")
        self.address = address
        return message

    def send(self, message: str, address: Any) -> None:
        self.sock.sendto(message.encode("utf-8"), address)

    def send_as_response(self, message: str) -> None:
        if self.address is None:
            raise RuntimeError("Cannot send as reponse without receiving first")
        self.send(message, self.address)
