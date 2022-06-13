"""Contains all message types along with their related string
"""

from enum import Enum

class MediatorMessageTypes(str, Enum):
    REQ_TR_SAVE = "TR_SAVE"
    REQ_TR_REGISTER = "REGISTER"
    REQ_TR_END_SAVE = "END_TR_SAVE"
    
    RESP_ACK = "RESP_REGISTER"
    RESP_TR_SAVE = "RESP_TR_SAVE"
    RESP_END_TR_SAVE = "RESP_END_TR_SAVE"

    GET_PATH_LIST = "GET_PATH_LIST"
    RESP_PATH_LIST = "RESP_PATH_LIST"
    GET_ONE_PATH = "GET_ONE_PATH"
    RESP_ONE_PATH = "RESP_ONE_PATH"

    TR_LAUNCH = "TR_LAUNCH"
    RESP_TR_LAUNCH = "RESP_TR_LAUNCH"
    REQ_TR_POINTS = "REQ_TR_POINTS"
    RESP_REQ_TRIP_POINTS = "RESP_REQ_TRIP_POINTS"
    WAIT_TR_FILE = "WAIT_TR_FILE"
    TR_FILE = "TR_FILE"
    RESP_TR_FILE = "RESP_TR_FILE"
    NEXTDRONEPOSITION = "NEXTDRONEPOSITION"
    RESP_DRONEPOSITION = "RESP_DRONEPOSITION"
    TR_ERROR = "TR_ERROR"
    END_TR_ERROR = "END_TR_ERROR"
    ERROR_NOTIFICATION_RECEIVED = "ERROR_NOTIFICATION_RECEIVED"
    DRONEPOSITION = "DRONEPOSITION"
    END_TR_LAUNCH = "END_TR_LAUNCH"
    RESP_END_TR_LAUNCH = "RESP_END_TR_LAUNCH"


    @staticmethod
    def find_from_value(value: str) -> "MediatorMessageTypes":
        msg_type = next((m for m in MediatorMessageTypes if m.value == value), None)
        if msg_type is None:
            raise ValueError(f"Cannot find {value} in the MediatorMessageTypes")
        return msg_type