from socket import *
import TicTacToe.py
import threading


HOST = '127.0.0.1' #localhost
PORT = 5000        #port

def sendMove(row, col):
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((HOST, PORT))
    move = f"{row},{col}"
    client.sendall(move.encode())
    data = client.recv(1024)
    client.close()
