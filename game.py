class Game:
    def __init__(self, id):
        self.BOARD_ROWS = 3
        self.BOARD_COLS = 3
        self.playerTurn = 0
        self.ready = False
        self.id = id
        self.winner = 0
        self.messages = []
        self.board = [['' for _ in range(self.BOARD_COLS)] for _ in range(self.BOARD_ROWS)]

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def check_player_win(self, mark):
        for row in range(self.BOARD_ROWS):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] == mark:
                return True

        for col in range(self.BOARD_COLS):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == mark:
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] == mark:
            return True

        if self.board[0][2] == self.board[1][1] == self.board[2][0] == mark:
            return True

        return False
    
    def checkTie(self):
        temp = 0
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if self.board[row][col] == 'X' or self.board[row][col] == 'O':
                    temp += 1
        if temp == 9:
            return True
        return False
    
    def check_win(self):
        if self.check_player_win("X"):
            self.winner = 0
            return True
        if self.check_player_win("O"):
            self.winner = 1
            return True
        return False
    
    def changeTurn(self):
        if(self.playerTurn == 0):
            self.playerTurn = 1
        else:
            self.playerTurn = 0
    
    def resetGame(self):
        self.BOARD_ROWS = 3
        self.BOARD_COLS = 3
        self.playerTurn = 0
        self.ready = True
        self.winner = 0
        self.messages = []
        self.board = [['' for _ in range(self.BOARD_COLS)] for _ in range(self.BOARD_ROWS)]