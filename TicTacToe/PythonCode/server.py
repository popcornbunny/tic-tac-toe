from socket import *
import TicTacToe.py
import threading

HOST = '127.0.0.1' #localhost
PORT = 5000        #port

clients = []
game = TicTacToe.__init__(p1)

def handleClient(client, addr):
    print('Connected to', addr)
    while True:
        data = client.recv(1024)
        if not data:
            break
        msg = data.decode()
        row, col = msg.split(',')

        valid = false
        while not valid:
            if TicTacToe.makeMove(game, row, col):
                valid = true
            else:
                client.sendall(b'Invalid move, pick another space.')
                data = client.recv(1024)
                msg = data.decode()
                row, col = msg.split(',')

        client.sendall(data)
    client.close()

def startServer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('Server started on port', PORT)
        while True:
            client, addr = s.accept()
            clients.append(client)
            threading.Thread(target=handleClient, args=(client, addr)).start()

   