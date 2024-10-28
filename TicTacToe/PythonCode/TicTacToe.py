from socket import *
# ask user for IP if it is an "online" game
#use section 2.7 of the book for the server and client code
# create a server and client python file (server.py and client.py)

#  This class provides support for playing a Tic Tac Toe game,
#  but doesn't enforce which player goes when.  It does protect
#  the board so a player can't change another player's move or
#  mark the same place twice.
#
# Author: Dr. Girard
# Edited by Katelyn Hanft

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
        self.initializeBoard()
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
        success = False
        if self.game_board[r][c] == ' ':
            if self.player_move == 0:
                self.game_board[r][c] = 'O'
                success = True
            if self.player_move == 1:
                self.game_board[r][c] = 'X'
                success = True
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
    
        for c in range(self.max):
            if (board[0][c] == win_token) and (board[1][c] == win_token) and (board[2][c] == win_token):
                win = True

        if (board[0][0] == win_token) and (board[1][1] == win_token) and (board[2][2] == win_token):
            win = True

        if (board[0][2] == win_token) and (board[1][1] == win_token) and (board[2][0] == win_token):
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

def play(p1, p2):
    __init__(newGame)
    initializeBoard(newGame)

    setPlayer(newGame, 0)  # Player 1 is 'O'
    setPlayer(newGame, 1)  # Player 2 is 'X'

    while not checkForWin(newGame):
        if checkForWin(p2):
            print("Congrats, Player 2 won!")
            resetGame(p1)
            resetGame(p2)
        else:
            r, c = input("Player 1's turn! (# #) ").split()
            makeMove(p1, r, c)
            toString(p1)

        if checkForWin(p1):
            print("Congrats, Player 1 won!")
            resetGame(p1)
            resetGame(p2)
        else:
            r, c = input("Player 2's turn! (# #) ").split()
            makeMove(p2, r, c)
            toString(p2)

