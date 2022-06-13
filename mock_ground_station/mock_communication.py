""" This script will permit to test the app without the server on :
it will receive requests and send aswers accordingly to the specs
"""
from typing import Callable, Dict
from loguru import logger
from time import sleep
from random import randint
from pathlib import Path

import sys
sys.path.append(Path(__file__).resolve().parents[1].as_posix())
# Must be put after sys.path.append
from library import * # noqa

SEND_PORT = 6870
RECEIVE_PORT = 6869

udp_socket = UdpSocket(RECEIVE_PORT)
drone = Drone()

def handle_ack(ack_msg: Message, send_address: Tuple[str, int]):
    sleep(0.1)
    send_message(udp_socket, create_answer(MessageTypes.RESP_ACK), send_address)

def handle_start_drone(start_msg: Message, send_address: Tuple[str, int]):
    drone.armed = True
    send_message(udp_socket, create_answer(MessageTypes.RESP_START_DRONE), send_address)

def handle_record(record_msg: Message, send_address: Tuple[str, int]):
    record = record_msg.content["record"]
    if record == drone.recording:
        send_message(udp_socket, create_answer(MessageTypes.RESP_RECORD, False, "Record already in wanted state"), send_address)
    else:
        drone.recording = record
        send_message(udp_socket, create_answer(MessageTypes.RESP_RECORD), send_address)

def handle_manual(manual_msg: Message, send_address: Tuple[str, int]):
    content = manual_msg.content
    x, y, z, r = content["x"], content["y"], content["z"], content["r"]
    logger.info(f"Move with command {(x, y, z, r)}")
    drone.move(x, y, z, r)

def handle_drone_infos(infos_msg: Message, send_address: Tuple[str, int]):
    send_message(udp_socket, create_drone_infos_resp(drone), send_address)

# This dict contains all functions for each request
HANDLERS: Dict[MessageTypes, Callable[[Message, Tuple[str, int]], None]] = {
    MessageTypes.REQ_ACK: handle_ack,
    MessageTypes.REQ_START_DRONE: handle_start_drone,
    MessageTypes.REQ_MANUAL_CONTROL: handle_manual,
    MessageTypes.REQ_RECORD: handle_record,
    MessageTypes.REQ_DRONE_INFOS: handle_drone_infos
}

def main():
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    while "waiting for messages":
        message = receive_message(udp_socket)
        # We must set the destination address in order to change the send port
        SEND_ADDRESS = (udp_socket.address[0], SEND_PORT)
        
        handleFunc = HANDLERS[message.type]
        handleFunc(message, SEND_ADDRESS)


if __name__ == "__main__":
    main()
