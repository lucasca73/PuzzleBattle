from server import WebsocketServer
import sys
from multiprocessing import Process
import Queue
import time
import random


def sendMessage(message):
	print(message)
	ws.websocket.send_message_to_all(message)
 
if __name__ == '__main__':
    ws = WebsocketServer()

    # handling new process
    p = Process(target=WebsocketServer.start, args = (ws,))
    p.start()

    print("\nThread is running async")

    try:
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        print('Keyboard interrupt')
        p.terminate()
        sys.exit(0)