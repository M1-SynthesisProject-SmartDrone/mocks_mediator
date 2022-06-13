import asyncio
import traceback
from typing import Union
from loguru import logger

from pynput.keyboard import Key, KeyCode, Listener

def transmit_keys() -> asyncio.Queue:
    """Create an event queue that will receive all keypresses
    """
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    def on_press(key):
        loop.call_soon_threadsafe(queue.put_nowait, key)

    def on_release(key):
        pass
        # loop.call_soon_threadsafe(queue.put_nowait, key.char)

    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()

    return queue


async def task_handle_keys():
    key_queue = transmit_keys()
    while True:
        key = await key_queue.get()
        key.char
        if key == Key.esc:
            logger.info("End task !")
            break
        logger.info(f"Read key {key}")

async def task_sleeps():
    while True:
        await asyncio.sleep(1)
        logger.debug("BOOP")

async def main():
    task1 = asyncio.create_task(task_handle_keys())
    task2 = asyncio.create_task(task_sleeps())

    
    try:
        await task1
    except Exception as e:
        logger.error(f"Error in task 1 : {e}")
        task1.cancel()
    finally:
        task2.cancel()

asyncio.run(main())