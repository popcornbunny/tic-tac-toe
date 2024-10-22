from socket import *
# ask user for IP if it is an "online" game
#use section 2.7 of the book for the server and client code
# create a server and client python file (server.py and client.py)

#  This class provides support for playing a Tic Tac Toe game,
#  but doesn't enforce which player goes when.  It does protect
#  the board so a player can't change another player's move or
#  mark the same place twice.
class TicTacToe:
    max = 3
##	  ' ' - Blank place
##	  'O' - 'O' Player controls that spot
##	  'X' - 'X' Player controls that spot
    game_board = []
    
##	  -1 = game not started
##	  0 = 'O' Player
##	  1 = 'X' Player
    player_move = -1

    def __init__(self):
        self.initializeBoard()

# Sets all the places on the board to blank.
    def initializeBoard(self):
        for r in range(self.max):
            new_row = []
            for c in range(self.max):
                new_row.append(' ')
            self.game_board.append(new_row)

    def resetGame(self):
        self.game_board.clear()
        initializeBoard(self)
        self.player_move = -1

    def setPlayer(self, player):
        if player == -1:
            self.player_move = -1
        elif player == 0:
            self.player_move = 0
        elif player == 1:
            self.player_move = 1
        else:
            self.player_move = -1

    def getPlayer(self):
        return self.player_move


##	  Will update the game_board based on location and
##	  which player is actively moving.  Will not update a location
##	  if a player has already played there or if player_move is
##	  set to -1.
##	  @param r Row player is making a move.
##	  @param c Column player is making a move.
##	  @return True if the game_board was updated, false otherwise.
    def makeMove(self, r, c):
        success = false
        if game_board[r][c] == ' ':
            if player_move == 0:
                self.game_board[r][c] = 'O'
                success = true
            if player_move == 1:
                self.game_board[r][c] = 'X'
                success = true
        return success


##	 Checks to see if the player_move player has won.
##	 @return true if the player has won, false otherwise.
    def checkForWin(self):
        win = False
        win_token = '-'
        if self.player_move == 0:
            win_token = 'O'
        if self.player_move == 1:
            win_token = 'X'

        board = self.game_board
        for r in range(self.max):
            if (board[r][0] == win_token) and (board[r][1] == win_token) and (board[r][2] == win_token):
                win = True
    
        for c in range(self.__max):
            if (board[0][c] == win_token) and (board[1][c] == win_token) and (board[2][c] == win_token):
                win = True

        if (board[0][0] == win_token) and (board[1][1] == win_token) and (board[2][2] == win_token):
            win = True

        if (game_board[0][2] == win_token) and (board[1][1] == win_token) and (board[2][0] == win_token):
            win = True
        return win



##	  @return The state of the board.
    def toString(self):
        board = "-------\n"
        for r in range(self.max):
            for c in range(self.max):
                board += "|" + self.game_board[r][c]
            board += "|\n"
            board += "-------\n"
        return board

class Play:
    TicTacToe.__init__(p1)
    TicTacToe.initializeBoard(p1)

    TicTacToe.__init__(p2)
    TicTacToe.initializeBoard(p2)

    net = input("Would you like to play over the network? (Y/N) ")

    if net == 'N' or net == 'n' or net == 'No' or net == 'no':
        print("Player 1, you are 0! Player 2, you are X!")
        TicTacToe.setPlayer(p1, 0)
        TicTacToe.setPlayer(p2, 1)

        while not TicTacToe.checkForWin(p1) or not TicTacToe.checkForWin(p2):
            if TicTacToe.checkForWin(p2):
                print("Congrats, Player 2 won!")
                TicTacToe.resetGame(p1)
                TicTacToe.resetGame(p2)
            else:
                r, c = input("Player 1's turn! (# #) ").split()
                TicTacToe.makeMove(p1, r, c)
                TicTacToe.toString(p1)

            if TicTacToe.checkForWin(p1):
                print("Congrats, Player 1 won!")
                TicTacToe.resetGame(p1)
                TicTacToe.resetGame(p2)
            else:
                r, c = input("Player 2's turn! (# #) ").split()
                TicTacToe.makeMove(p2, r, c)
                TicTacToe.toString(p2)

