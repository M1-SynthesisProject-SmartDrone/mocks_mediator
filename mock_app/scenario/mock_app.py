""" This script will permit to test the server without using the app :
it will receive requests and send aswers accordingly to the specs
"""
from loguru import logger
from time import sleep, time
from random import randint
from pathlib import Path

import sys
sys.path.append(Path(__file__).resolve().parents[2].as_posix())
# Must be put after sys.path.append
from library import * # noqa

# Two ports are useful when the server is on the same computer...
SEND_PORT = 6869
RECEIVE_PORT = 6870
SERVER_IP_ADDRESS = "127.0.0.1"

SEND_ADDRESS = (SERVER_IP_ADDRESS, SEND_PORT)

udp_socket = UdpSocket(RECEIVE_PORT)

def init_communication():
    logger.info("Send ACK")
    ack_answer = send_receive(udp_socket, create_ack(), MessageTypes.RESP_ACK, SEND_ADDRESS)
    ack_answer.assert_validated()
    logger.info("Positive answer received !")

    logger.info("Ask drone infos")
    drone_infos = send_receive(udp_socket, create_drone_infos(), MessageTypes.RESP_DRONE_INFOS, SEND_ADDRESS)

    logger.info("Send START_DRONE command")
    start_answer = send_receive(udp_socket, create_start_drone(), MessageTypes.RESP_START_DRONE, SEND_ADDRESS)
    start_answer.assert_validated()
    logger.info("Positive answer received !")

def test_simple_fly():
    """ In this test, we do not receive any messages, but the drone should be disarmed at the end
    """
    # Put motors at max in order to start motors
    send_message(udp_socket, create_manual_control(z=1.0), SEND_ADDRESS)
    time_start = time()
    # Up for 10 seconds
    logger.info("Take off !")
    while (time() - time_start) < 10.0:
        sleep(0.2)
        # Not too high !
        send_message(udp_socket, create_manual_control(z=0.1), SEND_ADDRESS)
    time_start = time()
    # Go down and disarm (normally)
    logger.info("Land")
    while (time() - time_start) < 20.0:
        sleep(0.2)
        send_message(udp_socket, create_manual_control(z=-1.0), SEND_ADDRESS)

    drone_infos = send_receive(udp_socket, create_drone_infos(), MessageTypes.RESP_DRONE_INFOS, SEND_ADDRESS)

def main():
    init_communication()
    test_simple_fly()

if __name__ == "__main__":
    main()