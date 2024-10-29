# Client side of the TicTacToe game
# Authors: Katelyn Hanft and Faith Wilson

import socket
import TicTacToe

# First player to connect is player 1, other is player 2
# Function to connect to the server and play the game
def runClient(host, port):
    print("Connecting to the Tic-Tac-Toe server...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("Connected to server at " + host + " on port " + str(port))
        msg = s.recv(1024).decode()

        while "win" not in msg or "draw" not in msg:
            if msg is not None:
                print(msg)
            else:
                print("Goodbye!")
                s.close()
                break
            if "Enter your move" in msg:
                move = input()
                s.sendall(move.encode())
            if "play again" in msg:
                s.sendall(input().encode())

            msg = s.recv(1024).decode()

        # If the game is over, close the connection
        s.close()
        print("\nGame over. Closing connection.")

# Main function to run the client
def main():
    serverHost = input("Enter the IP address you want to connect to: ")
    serverPort = int(input("Enter the port number: "))

    runClient(serverHost, serverPort)

if __name__ == "__main__":
    main()
