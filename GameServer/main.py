from websocket import WebsocketServer
from Game import *
import sys
from multiprocessing import Process
import threading
import time

 
if __name__ == '__main__':
    ws = WebsocketServer()
    game = Game(ws)

    # handling new process
    t = threading.Thread(target=WebsocketServer.start, args = (ws,))
    t.daemon = True
    t.start()

    print("\nThread is running async")


    try:
        while True:
            game.update()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('\nEnding server\n')
        sys.exit(0)