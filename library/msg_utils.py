from random import randint
from typing import Any, Tuple
from loguru import logger


from library.Message import Message
from library.MessageTypes import MessageTypes
from library.UdpSocket import UdpSocket
from library.Drone import Drone

# ==== MAIN ====
def send_receive(
    udp_socket: UdpSocket, 
    message: Message, 
    wanted_type: MessageTypes, 
    address: Tuple[str, int]) -> Message:

    """ Send a message and wait for the answer
    """
    udp_socket.send(message.toJsonStr(), address)
    response = receive_message(udp_socket, wanted_type)
    return response

# ==== RECEIVE ====
def receive_message(udp_socket: UdpSocket, wanted_type: MessageTypes = None) -> Message:
    message = Message.fromStr(udp_socket.receive())
    if wanted_type is not None and message.type != wanted_type:
        raise ValueError(f"Didn't receive the wanted type. Expected {wanted_type} but got {message.type}")
    return message

# ==== SEND ====
def send_message(udp_socket: UdpSocket, message: Message, address: Tuple[str, int] = None) -> None:
    udp_socket.send(message.toJsonStr(), address)

# ===== CREATE REQ MESSAGES ====
def create_ack() -> Message:
    return Message(MessageTypes.REQ_ACK, {})

def create_drone_infos() -> Message:
    return Message(MessageTypes.REQ_DRONE_INFOS, {})

def create_start_drone() -> Message:
    return Message(MessageTypes.REQ_START_DRONE, {"startDrone": True})

def create_manual_control(x=0.0, y=0.0, z=0.0, r=0.0) -> Message:
    return Message(MessageTypes.REQ_MANUAL_CONTROL, {
        "x": x,
        "y": y,
        "z": z,
        "r": r
    })

# ==== CREATE RESP MESSAGES ====
def create_answer(msg_type: MessageTypes, validated: bool = True, msg_str: str = "") -> Message:
    return Message(msg_type, {
        "validated": validated,
        "message": msg_str
    })

def create_drone_infos_resp(drone: Drone = None) -> Message:
    if drone is None:
        return Message(MessageTypes.RESP_DRONE_INFOS, {
            "armed": True,
            "recording": True,
            "batteryRemaining": randint(0, 100),
            "lat": randint(100000000, 500000000),
            "lon": randint(100000000, 500000000),
            "alt": randint(1000, 2000),
            "relativeAlt": randint(100, 200),
            "vx": randint(0, 50),
            "vy": randint(0, 50),
            "vz": randint(0, 50),
            "yawRotation": randint(0, 364)
        })
    else:
        return Message(MessageTypes.RESP_DRONE_INFOS, {
            "armed": drone.armed,
            "recording": drone.recording,
            "batteryRemaining": drone.battery_remaining,
            "lat": drone.lat,
            "lon": drone.lon,
            "alt": drone.alt,
            "relativeAlt": drone.relative_alt,
            "vx": drone.vx,
            "vy": drone.vy,
            "vz": drone.vz,
            "yawRotation": drone.yaw_rotation
        })