""" This script will permits to emulate the ground station behavior :
it will :
 - connect to the server
 - send a TR_SAVE request
 - after confirmation, send multiple TR_REGISTER requests (with images)
 - after a certain amount of time, send a TR_END_SAVE request
"""
import json
from typing import Callable, Dict
from loguru import logger
from time import sleep, time
from random import randint, random
from pathlib import Path
import cv2
import threading

import sys
sys.path.append(Path(__file__).resolve().parents[1].as_posix())
# Must be put after sys.path.append
from library import * # noqa

PORT = 7000
IP_ADDRESS = "127.0.0.1"
PORT2 = 7001

img = cv2.imread("/home/nico/Bureau/Fac/M1/S1/pds-mocks/mock_groundstation_for_mediator/test.png")
img_size = img.nbytes

tcp = TcpSocket()
tcp2 = TcpSocket()

def create_msg(type: MediatorMessageTypes, content: dict) -> MediatorMessage:
    content["requestType"] = type.value
    return MediatorMessage(type, content)


def send_receive(socket: TcpSocket, 
    message: MediatorMessage, 
    wanted_return_type: MediatorMessageTypes) -> MediatorMessage:
    s = message.toJsonStr()
    logger.info(f"Send \"{s}\"")
    socket.send(s)
    resp = MediatorMessage.receive(socket)
    if resp.type.value != wanted_return_type.value:
        raise ValueError(f"Wanted {wanted_return_type.value} but got {resp.type.value}")
    return resp

def thread_receive()-> None:
        dataReceived = send_receive(tcp2, create_msg(MediatorMessageTypes.REQ_TR_POINTS, {}), MediatorMessageTypes.RESP_REQ_TRIP_POINTS)
        # filesize = dataReceived.content["filesize"]
        trFile = send_receive(tcp2, create_msg(MediatorMessageTypes.WAIT_TR_FILE, {}), MediatorMessageTypes.TR_FILE)
        print(trFile)
        pointList = trFile.content["content"]
        print("trFile : {trFile}")
        size = len(pointList)
        print(f"len {size}")
        tcp2.send(create_msg(MediatorMessageTypes.RESP_TR_FILE, {}).toJsonStr()) 
        for index in range(size ):
            sleep(1)
            print("send nextdronepos")
            # tcp2.send(create_msg(MediatorMessageTypes.NEXTDRONEPOSITION, {}).toJsonStr())
            trFile = send_receive(tcp2, create_msg(MediatorMessageTypes.NEXTDRONEPOSITION, {}), MediatorMessageTypes.DRONEPOSITION)
            # print(trFile.content)
            imagesize = trFile.content["imagesize"]
            print("send resp dronepos")
            tcp2.send(create_msg(MediatorMessageTypes.RESP_DRONEPOSITION, {}).toJsonStr()) 
            # filesize = json.load( trFile)["imagesize"]
            receivedImage = tcp2.receive_bytes(imagesize)
            print(receivedImage)



def thread_send()-> None:
    print("thread send")
    SEND_PERIOD = 0.1
    elapsed = 1000
    for index in range(10):
        print(elapsed)
        # if elapsed < SEND_PERIOD:
        #     sleep(SEND_PERIOD - elapsed)
        start = time()
        # The actual process
        # TODO : do some modifications on image in order to see changes ?
        register_msg = register_message(img_size)
        resp_ack = send_receive(tcp, register_msg, MediatorMessageTypes.RESP_ACK)
        tcp.send_bytes(img.data.obj)

        end = time()
        elapsed = end - start
    print("--> say to server that image treatment has found an error")
    send_receive(tcp, create_msg(MediatorMessageTypes.TR_ERROR, {}), MediatorMessageTypes.ERROR_NOTIFICATION_RECEIVED)

    for index in range(5):
        print(elapsed)
        # if elapsed < SEND_PERIOD:
         #     sleep(SEND_PERIOD - elapsed)
        start = time()
        # The actual process
        # TODO : do some modifications on image in order to see changes ?
        register_msg = register_message(img_size)
        resp_ack = send_receive(tcp, register_msg, MediatorMessageTypes.RESP_ACK)
        tcp.send_bytes(img.data.obj)

        end = time()
        elapsed = end - start
    print("--> say to server thatit's the end of the error")

    send_receive(tcp, create_msg(MediatorMessageTypes.END_TR_ERROR, {}), MediatorMessageTypes.ERROR_NOTIFICATION_RECEIVED)

    for index in range(10):
        print(elapsed)
        # if elapsed < SEND_PERIOD:
         #     sleep(SEND_PERIOD - elapsed)
        start = time()
        # The actual process
        # TODO : do some modifications on image in order to see changes ?
        register_msg = register_message(img_size)
        resp_ack = send_receive(tcp, register_msg, MediatorMessageTypes.RESP_ACK)
        tcp.send_bytes(img.data.obj)

        end = time()
        elapsed = end - start
    send_receive(tcp, create_msg(MediatorMessageTypes.END_TR_LAUNCH, {}), MediatorMessageTypes.RESP_END_TR_LAUNCH)



def register_message(img_size: int) -> MediatorMessage:
    return create_msg(MediatorMessageTypes.REQ_TR_REGISTER, {
        "altitude": randint(0, 100),
        "latitude": randint(123456789, 999999999),
        "longitude": randint(123456789, 999999999),
        "rotation": randint(0, 65355),
        "temperature": random() * 15,
        "pressure": random() * 20,
        "batteryRemaining": randint(0, 100),
        "isCheckpoint": random() > 0.5,
        "time": int(round(time() * 1000)),
        "image": img_size
    })

def create_tripname() -> str:
    return f"trip_{int(round(time() * 1000))}"

def main():
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    

    tcp.connect(IP_ADDRESS, PORT)
    sleep(0.5)
    tcp2.connect(IP_ADDRESS, PORT2)

    print("----- MOCK FOR MEDIATOR -----")
    print("Possible request : \n - save --> Save a trip\n - pathlist --> get the pathList\n - onepath --> get one path\n - launch --> Launch a path")
    while "true": 

        # Step 1 : send the tr save request


        reqInp = input("Enter request you want to test :")
        if(reqInp ==  "save"):
            resp_save = send_receive(tcp, create_msg(MediatorMessageTypes.REQ_TR_SAVE, {}), MediatorMessageTypes.RESP_TR_SAVE)
            # Step 2 : send multiple images 
            NB_ITERATIONS = 20
            SEND_PERIOD = 0.1
            elapsed = 1000
            for index in range(NB_ITERATIONS):
                print(elapsed)
                # if elapsed < SEND_PERIOD:
                #     sleep(SEND_PERIOD - elapsed)
                start = time()
                # The actual process
                # TODO : do some modifications on image in order to see changes ?
                register_msg = register_message(img_size)
                resp_ack = send_receive(tcp, register_msg, MediatorMessageTypes.RESP_ACK)
                tcp.send_bytes(img.data.obj)

                end = time()
                elapsed = end - start
                print(f"Sent in {elapsed} seconds")
            resp_end_save = send_receive(tcp, 
                create_msg(MediatorMessageTypes.REQ_TR_END_SAVE, 
                {"tripName": create_tripname()}), 
                MediatorMessageTypes.RESP_END_TR_SAVE
            )
        elif(reqInp == "pathlist"):
            resp_save = send_receive(tcp, create_msg(MediatorMessageTypes.GET_PATH_LIST, {}), MediatorMessageTypes.RESP_PATH_LIST)
            print(resp_save)
            
        elif(reqInp == "onepath"):
            # get path 46
                resp_save = send_receive(tcp, create_msg(MediatorMessageTypes.GET_ONE_PATH, {	"tr_id" : 46}), MediatorMessageTypes.RESP_ONE_PATH)
                print(resp_save)

        elif(reqInp == "launch"):
            resp_save = send_receive(tcp, create_msg(MediatorMessageTypes.TR_LAUNCH, {	"tr_id" : 46}), MediatorMessageTypes.RESP_TR_LAUNCH)
            # thread_receive()
            # thread_send()
            thread_recv = threading.Thread(target=thread_receive)
            thread_snd = threading.Thread(target=thread_send)
            thread_recv.start()
            thread_snd.start()
            for t in (thread_recv, thread_snd):
                t.join()
        else :
            print("NOT IMPLEMENTED OR ERROR \n Possible request : \n - save --> Save a trip\n - pathlist --> get the pathList\n - onepath --> get one path\n - launch --> Launch a path")

    # while "attente infinie":
    #     pass



if __name__ == "__main__":
    main()