import json

class Game():
    def __init__(self, ws):
        self.ws = ws
        self.handler = MessageHandler()
        self.playersGame = []

        self.ws.on_message = self.handler.handleMessage
        self.ws.on_closed  = self.player_leave
        self.ws.on_enter   = self.new_player

        self.setupHandler()

    def setupHandler(self):
        self.handler.addHandler('input', self.playerInput)
        self.handler.addHandler('check', self.checkState)

    def update(self):
        for p_game in self.playersGame:
            p_game.update()

    def new_player(self, client):
        new = PlayerGame(client)
        self.playersGame.append(new)

    def player_leave(self, client):
        print('player leave: ' + str(client['id']) )

    def reportGameState(self, client):
        gameState = {'state':1}
        strGameState = json.dumps(gameState)
        # turn string into json => json.loads( strJSON )
        ws.websocket.send_message_to_all(strGameState)
        pass

    def checkState(self, array_msg):
        print('check: ' + array_msg[0])

    def playerInput(self, array_msg):
        print('input: ' + array_msg[0])

class MessageHandler():
    
    def __init__(self):
        self.handlers = {}

    def handleMessage(self, message, client):
        array_msg = message.split(',')
        command = array_msg[0]
        try:
            self.handlers[command](array_msg)
        except KeyError, TypeError:
            print('[ERROR] command not registered: ' + command)

    def addHandler(self, command, handler):
        self.handlers[command] = handler

    def removeHandler(self, command):
        self.handlers[command] = None
        self.handlers.pop(command)

class PlayerGame():
    def __init__(self, client):
        self.client = client

    def update(self):
        pass

    def getJsonState(self):
        return {'game':1}

