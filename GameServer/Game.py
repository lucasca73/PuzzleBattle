import json
import os
import time

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


class Game():
    def __init__(self, ws):
        self.ws = ws
        self.handler = MessageHandler()
        self.playersGame = []
        
        self.player = PlayerGame(1)

        self.ws.on_message = self.handler.handleMessage
        self.ws.on_closed  = self.player_leave
        self.ws.on_enter   = self.new_player

        self.setupHandler()

    def setupHandler(self):
        self.handler.addHandler('input', self.playerInput)
        self.handler.addHandler('check', self.checkState)

    def update(self):
        # for p_game in self.playersGame:
        #     p_game.update()

        self.player.update()
        self.player.showTerminal()
        

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
    def __init__(self, client, rows=15, cols=15):
        self.client = client
        self.matrix = []
        self.n_rows = rows
        self.n_cols = cols
        
        self.it = 1

        self.setupMatrix()

    def placeholder(self):
        if self.it > 0:
            self.it -= 1
        else:
            self.it = 20

    def update(self):
        time.sleep(0.5)
        self.placeholder()

        if self.it == 0:
            self.matrix[0][self.n_cols/2] = 2

        for cols in self.matrix:
            for cell in cols:
                pass
        self.updateGravity()
        

    def updateGravity(self):

        later = []

        for row in range(0, self.n_rows):
            for col in range(0, self.n_cols):
                if self.matrix[col][row] == 2:
                    if self.checkCell(col+1, row) == 1:
                        def getDown(col, row):
                            self.matrix[col][row] = 0
                            self.matrix[col+1][row] = 2
                        later.append( (getDown, col, row) )

        for laterUpt in later:
            laterUpt[0](laterUpt[1],laterUpt[2])
                        

    def showTerminal(self):

        board = '\n\n\t- - - - - - - - -\n'
        for row in self.matrix:
            board += self.printRow(row)
        
        board += '\t- - - - - - - - -'
        clearScreen()
        print(board)
        

    def printRow(self, row):
        rowStr = '\t|'
        for cell in row:
            rowStr += ' ' if cell == 0 else '#'

        rowStr += '|\n'
        
        return rowStr

    def checkCell(self, col, row):

        result = 1 # should move

        limit = self.checkLimits(col, row)
        if limit != 1:
            return -1 # cant move by boundaries

        if self.matrix[col][row] == 1:
            result = 2 # this is a grounded piece 

        return result
    
    def checkLimits(self, col ,row):
        result = 1
        r_col = 1
        r_row = 1

        # Check limits
        if col >= len(self.matrix) or col < 0:
            r_col = -1
            
        if row >= len(self.matrix[0]) or row < 0:
            r_row = -1

        if r_col == -1 and r_row == -1:
            result = -3
        elif r_col == -1:
            result = -2 # cant move up or down
        elif r_row == -1:
            result = -1 # cant move right or left

        return result

    def setupMatrix(self):

        for set_col in range(0, self.n_rows):
            self.matrix.append([]) # Adding col
            for set_row in range(0, self.n_cols):
                self.matrix[set_col].append(0) # Adding row


    def getJsonState(self):
        return {'game':1}

