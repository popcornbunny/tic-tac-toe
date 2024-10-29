# Server for TicTacToe game
# Authors: Katelyn Hanft and Faith Wilson

import socket
import TicTacToe

host = socket.gethostbyname(socket.gethostname())  # gets IP Address of localhost

# Log file that stores each move
logFile = "log.txt"
def clearLog():
    global logFile
    with open(logFile, "w") as log:
        log.write("TicTacToe Game Log\n\n")  # clears the log file
        log.close()

# Starts a new game of TicTacToe
game = TicTacToe.TicTacToe()

# Starts the server and connects to two players
def startServer(port):
    global game
    game.resetGame()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
        # Starts the server and listens for incoming connections/clients
        ss.bind((host, int(port)))
        ss.listen()
        print('Server started on IP', socket.gethostbyname(socket.gethostname()), "with port", str(port))
        # Accepts two players/clients
        player1, addr1 = ss.accept()
        print(f"Connected to Player 1 at {addr1}")
        player1.sendall("Welcome, you are Player 1".encode())

        player2, addr2 = ss.accept()
        print(f"Connected to Player 2 at {addr2}")
        player2.sendall("Welcome, you are Player 2".encode())
    return player1, addr1, player2, addr2, ss


# Plays the game of TicTacToe between two players and logs each move
def playGame(p1, a1, p2, a2):
    moves = 0
    currentPlayer = 0
    running = True

    clearLog()
    p1.sendall("\n*A new game is beginning*\n".encode())
    p2.sendall("\n*A new game is beginning*\n".encode())

    while running:
        if currentPlayer == 0:
            player = p1
        else:
            player = p2

        player.sendall("Player 0: 0       Player 1: X\n".encode())
        player.sendall(("It is your turn Player " + str(currentPlayer + 1)).encode() + "\n".encode())
        player.sendall("Enter your move (row col): ".encode())

        print("Waiting for Player", currentPlayer + 1, "to make a move...")

        # Receive the move from the player
        move = player.recv(1024).decode()
        print("Player ", currentPlayer + 1, " entered move: ", move)

        # Check if the move is valid
        moveRaC = move.split(" ")
        if len(moveRaC) != 2:
            player.sendall("Invalid move, try again".encode())
            continue
        row = int(moveRaC[0])
        col = int(moveRaC[1])
        if row < 0 or row > 2 or col < 0 or col > 2:
            player.sendall("Invalid move, try again".encode())
            continue

        game.setPlayer(currentPlayer)
        if game.makeMove(row, col):
            moves = moves + 1  # Increment the number of moves made to check if all spots are filled
            ip1 = a1[0]
            ip2 = a2[0]
            # Log each move along with IP addresses
            entry = "Current player " + str(currentPlayer+1) + " (ip: " + ip1 + ") made a move at row " \
                    + str(row) + " and column " + str(col) + " against " + ip2
            p1.sendall(entry.encode())
            p2.sendall(entry.encode())
            logMove(entry)

            # Check if the game is won or not
            if game.checkForWin():
                player.sendall("You are the winner!\n".encode())
                if currentPlayer == 0:
                    p2.sendall("You have lost\n".encode())
                else:
                    p1.sendall("You have lost\n".encode())
                running = False
            elif moves == 9:
                p1.sendall("The game is a draw!\n".encode())
                p2.sendall("The game is a draw!\n".encode())
                running = False
            else:
                if currentPlayer == 0:
                    currentPlayer = 1
                else:
                    currentPlayer = 0
        else:
            player.sendall("Invalid move, try again".encode())

        # Sends the board
        p1.sendall(game.toString().encode())
        p2.sendall(game.toString().encode())

    p1.sendall("Do you want to play again? (yes/no): ".encode())
    p2.sendall("Do you want to play again? (yes/no): ".encode())
    new1 = p1.recv(1024).decode()
    new2 = p2.recv(1024).decode()
    if new1 == "yes" and new2 == "yes":
        game.resetGame()
        playGame(p1, a1, p2, a2)
    else:
        p1.sendall("Thanks for playing! ".encode())
        p2.sendall("Thanks for playing! ".encode())
        #p1.close()
        #p2.close()
        print("Server closed, game over.")
        return

# Logs each move made by the players
def logMove(entry):
    print(entry)
    with open(logFile, "a") as log:
        log.write(entry + "\n")
        log.close()

# Main function that starts the server and plays the game
def main():
    port = input("Please enter your port number: ")
    play1, a1, play2, a2, ss = startServer(port)
    playGame(play1, a1, play2, a2)
    ss.close()

if __name__ == "__main__":
    main()
