"""Contains all message types along with their related string
"""

from enum import Enum
from typing import Optional

class MessageTypes(str, Enum):
    REQ_ACK = "ACK"
    REQ_START_DRONE = "START_DRONE"
    REQ_RECORD = "RECORD"
    REQ_MANUAL_CONTROL = "MANUAL_CONTROL"
    REQ_DRONE_INFOS = "DRONE_INFOS"
    
    RESP_ACK = "RESP_ACK"
    RESP_START_DRONE = "RESP_START_DRONE"
    RESP_RECORD = "RESP_RECORD"
    RESP_DRONE_INFOS = "RESP_DRONE_INFOS"

    @staticmethod
    def find_from_value(value: str) -> "MessageTypes":
        msg_type = next((m for m in MessageTypes if m.value == value), None)
        if msg_type is None:
            raise ValueError(f"Cannot find {value} in the MessageTypes")
        return msg_type