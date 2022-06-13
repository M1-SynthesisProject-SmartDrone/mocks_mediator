""" This script will permits to emulate the mediator behavior :
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

PORT = 7070
tcp = TcpSocket()

def main():
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    tcp.wait_connection(PORT)

    while "waiting for messages":

        pass

if __name__ == "__main__":
    main()