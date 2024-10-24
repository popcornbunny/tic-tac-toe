# Client side of the TicTacToe game
# Author: Katelyn Hanft

from socket import *
import TicTacToe.py
import threading

# First player to connect is player 1, other is player 2

def receiveData(sock):
    while True:
        try:
            data = sock.recv(1024).decode() #Receive data from the server
            if not data:
                break
            print(data)
            if ("Enter your move" in data):
                return # If it is the player's turn, return to allow input
        except socket.error:
            print("Error receiving data from the server")
            break

def main():
    serverHost = input("Enter the host IP address: ")
    serverPort = int(input("Enter the port number: "))

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create socket
        sock.connect((serverHost, serverPort)) #Connect to the server
        print("Connected to the server at ", serverHost, " on port ", serverPort)

        while True:
            receiveData(sock) #Display data from server
            move = input("Enter your move (row col): ") #Take move from user
            sock.sendall(move.encode()) #Send move to server

            receiveData(sock) #Display data from server

    except socket.error as e:
        print(f"Connection error: {e}")
    finally:
        sock.close() #Close the socket
        print("Connection closed")

if __name__ == "__main__":
    main()
