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

        # print(inputBuffer)

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
        # print('check: ' + array_msg[0])
        pass

    def playerInput(self, array_msg):
        # print('input: ' + array_msg[1])
        self.player.inputBuffer.append( str(array_msg[1]) ) 
        # print(self.player.inputBuffer)

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
        self.didLose = False
        self.currentPiece = (-1,-1)
        self.inputBuffer = []

        self.it = 5

        self.setupMatrix()

    def update(self):
        if self.didLose:
            return
        
        self.updateGravity()

        if len(self.inputBuffer) > 0:
            move = self.inputBuffer.pop()
            self.moveCurrentPiece(move)

        # time.sleep(0.5)

        # self.it -= 1
        # if self.it < 0:
        #     self.moveCurrentPiece('left')
        #     self.it = 5


        # Create new piece/ check if lost
        if self.currentPiece[0] == -1:
            if self.matrix[0][self.n_cols/2] == 1:
                self.lose()
            else:
                self.launchNewPiece()

    def updateGravity(self):

        later = []

        for row in range(0, self.n_rows):
            for col in range(0, self.n_cols):
                if self.matrix[col][row] == 2:
                    check = self.checkCell(col+1, row)
                    if check == 1:
                        later.append( (self.moveCurrentPiece, 'down') )
                    
                    # grounding pieces in the bottom
                    if check == -1 and col+1 >= self.n_cols:
                        self.groundCurrentPiece()
                    
                    # grounding pieces when touching other pieces
                    if check == 2:
                        self.groundCurrentPiece()

        for laterUpt in later:
            laterUpt[0](laterUpt[1])


    def showTerminal(self):

        if self.didLose:
            board = '\t  -- YOU LOSE --\n\n\t- - - - - - - - -\n'
        else:
            board = '\n\n\t- - - - - - - - -\n'
        for row in self.matrix:
            board += self.printRow(row)
        
        board += '\t- - - - - - - - -'
        clearScreen()
        print(board)
        

    def printRow(self, row):
        rowStr = '\t|'
        for cell in row:
            if cell == 1:
                rowStr += '@'
            elif cell == 2:
                rowStr += '#'
            else:
                rowStr += ' '
            

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


    def lose(self):
        self.didLose = True

    def moveCurrentPiece(self, move):

        if self.currentPiece[0] == -1:
            return

        c = self.currentPiece[0]
        r = self.currentPiece[1]

        if move == 'up':
            new_pos = (c-1,r)
        elif move == 'down':
            new_pos = (c+1,r)
        elif move == 'left':
            new_pos = (c,r-1)
        elif move == 'right':
            new_pos = (c,r+1)
        else:
            return

        # Check if can move
        if self.checkCell(new_pos[0], new_pos[1]) == 1:
            self.currentPiece = new_pos
        
        new_c = self.currentPiece[0]
        new_r = self.currentPiece[1]

        # Move piece
        self.matrix[c][r] = 0
        self.matrix[new_c][new_r] = 2

        pass

    def groundCurrentPiece(self):
        c = self.currentPiece[0]
        r = self.currentPiece[1]
        self.matrix[c][r] = 1
        self.currentPiece = (-1,-1)

    def launchNewPiece(self):
        self.currentPiece = (0,self.n_cols/2)
        c = self.currentPiece[0]
        r = self.currentPiece[1]
        self.matrix[c][r] = 2


    def getJsonState(self):
        return {'game':1}

