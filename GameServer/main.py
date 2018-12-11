from websocket import WebsocketServer
from Game import Game
import sys
from multiprocessing import Process
import time

 
if __name__ == '__main__':
    ws = WebsocketServer()
    game = Game(ws)

    # handling new process
    p = Process(target=WebsocketServer.start, args = (ws,))
    p.start()

    print("\nThread is running async")

    


    try:
        while True:
            game.update()
            time.sleep(0.2)
    except KeyboardInterrupt:
        print('Keyboard interrupt')
        p.terminate()
        sys.exit(0)