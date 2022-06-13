""" This script will permit to test the server without using the app :
it will receive requests and send aswers accordingly to the specs
"""

# ! WARNING : DOES NOT WORK FOR THE MOMENT

from loguru import logger
from time import sleep, time
from random import randint
from pathlib import Path

import pynput
import asyncio

import sys
sys.path.append(Path(__file__).parents[1].as_posix())
# Must be put after sys.path.append
from library import * # noqa

# Two ports are useful when the server is on the same computer...
SEND_PORT = 6869
RECEIVE_PORT = 6870
SERVER_IP_ADDRESS = "127.0.0.1"

udp_socket = UdpSocket(RECEIVE_PORT)

def init_communication():
    logger.info("Send ACK")
    send_ack(udp_socket, SERVER_IP_ADDRESS, SEND_PORT)
    logger.info("Wait for the answer")
    receive_answer(udp_socket, need_positive=True)
    logger.info("Positive answer received !")

    logger.info("Send START_DRONE command")
    send_start_drone(udp_socket, SERVER_IP_ADDRESS, SEND_PORT)
    receive_answer(udp_socket, need_positive=True)
    logger.info("Positive answer received !")

def test_simple_fly():
    """ In this test, we do not receive any messages, but the drone should be disarmed at the end
    """
    # Put motors at max in order to start motors
    send_manual_control(udp_socket, SERVER_IP_ADDRESS, SEND_PORT, z=1.0)
    time_start = time()
    # Up for 10 seconds
    logger.info("Take off !")
    while (time() - time_start) < 10.0:
        # Not too high !
        send_manual_control(udp_socket, SERVER_IP_ADDRESS, SEND_PORT, z=0.1)
    time_start = time()
    # Go down and disarm (normally)
    logger.info("Land")
    while (time() - time_start) < 20.0:
        send_manual_control(udp_socket, SERVER_IP_ADDRESS, SEND_PORT, z=-1.0)

def main():
    init_communication()
    test_simple_fly()



    
    

if __name__ == "__main__":
    main()