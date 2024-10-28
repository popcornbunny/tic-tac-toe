# Server for TicTacToe game
# Authors: Katelyn Hanft and Faith Wilson

import socket
import TicTacToe

host = socket.gethostbyname(socket.gethostname())  # gets IP Address

# Log file that stores each move
logFile = "log.txt"

# Starts a new game of TicTacToe
game = TicTacToe.TicTacToe()

# Starts the server and connects to two players
def startServer(port):
    global game
    game.resetGame()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
        ss.bind((host, int(port)))
        ss.listen()
        print('Server started on IP', socket.gethostbyname(socket.gethostname()), "with port", str(port))

        player1, addr1 = ss.accept()
        print(f"Connected to Player 1 at {addr1}")
        player1.sendall("Welcome, you are Player 1".encode())

        player2, addr2 = ss.accept()
        print(f"Connected to Player 2 at {addr2}")
        player2.sendall("Welcome, you are Player 2".encode())
    return player1, addr1, player2, addr2

# Plays the game of TicTacToe between two players and logs each move
def playGame(p1, a1, p2, a2):
    currentPlayer = 0
    running = True

    while running:
        if currentPlayer == 0:
            player = p1
        else:
            player = p2

        player.sendall("Player 0: 0       Player 1: X".encode())
        player.sendall(("It is your turn Player " + str(currentPlayer)).encode() + "\n".encode())
        player.sendall("Enter your move (row col): ".encode())

        print("Waiting for player ", currentPlayer, " to make a move...")

        move = player.recv(1024).decode()
        print("Player ", currentPlayer, " entered move: ", move)

        moveRaC = move.split(" ")
        row = int(moveRaC[0])
        col = int(moveRaC[1])

        game.setPlayer(currentPlayer)
        if game.makeMove(row, col):
            ip1 = a1[0]
            ip2 = a2[0]

            entry = "Current player " + str(currentPlayer) + " ip: " + ip1 + " made a move at row " + str(row) + " and column " + str(col) + " against " + ip2
            p1.sendall(entry.encode())
            p2.sendall(entry.encode())
            logMove(entry)

            if game.checkForWin():
                player.sendall("You are the winner!\n".encode())
                if currentPlayer == 0:
                    p2.sendall("You have lost\n".encode())
                else:
                    p1.sendall("You have lost\n".encode())
                running = False
            else:
                if currentPlayer == 0:
                    currentPlayer = 1
                else:
                    currentPlayer = 0
        else:
            player.sendall("Invalid move, try again".encode())

        p1.sendall(game.toString().encode())
        p2.sendall(game.toString().encode()) # change to print tostring if needed
    p1.sendall("\n*A new game is beginning*\n".encode())
    p2.sendall("\n*A new game is beginning*\n".encode())
    game.resetGame()
    playGame()

    p1.close()
    p2.close()
    ss.close()

    print("Server closed, game over.")

# Logs each move made by the players
def logMove(entry):
    print(entry)
    with open(logFile, "a") as log:
        log.write(entry + "\n")

# Main function that starts the server and plays the game
def main():
    port = input("Please enter your port number: ")
    play1, a1, play2, a2 = startServer(port)
    playGame(play1, a1, play2, a2)

if __name__ == "__main__":
    main()
