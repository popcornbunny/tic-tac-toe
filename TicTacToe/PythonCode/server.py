# Server for TicTacToe game
# Author: Katelyn Hanft

from socket import *
import TicTacToe.py
import threading
#157.160.151.206
host = '127.0.0.1' #localhost - change to my IP
#port = 5000        #port

# Log to store each move
logFile = "log.txt"

game = TicTacToe.__init__(p1)

def startServer(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
        ss.bind((host, port))
        ss.listen()
        print('Server started on port', port)
        player1, addr1 = ss.accept()
        with player1:
            print(f"Connected to Player 1 at {addr1}")
        player2, addr2 = ss.accept()
        with player2:
            print(f"Connected to Player 2 at {addr2}")

        # Handle clients
        player1 = 0
        player2 = 1
        currentPlayer = player1
        running = True

        while running:
            print(f"Player 0: 0     Player 1: X")
            print(f"")




def main():
    startServer()

# ChatGPT

def handle_client(conn, addr, game, player_id):
    conn.sendall(f"Player 1: O, Player 2: X\n".encode('utf-8'))
    conn.sendall(f"Welcome Player {player_id}!\n".encode('utf-8'))
    while True:
        conn.sendall(f"Game Board:\n{game}\n".encode('utf-8'))
        conn.sendall(f"It is your turn, Player {player_id}. Enter your move (row col): ".encode('utf-8'))

        move = conn.recv(1024).decode('utf-8')
        try:
            row, col = map(int, move.split())
            game.set_player(player_id)

            if game.make_move(row, col):
                if game.check_for_win():
                    conn.sendall("You are the winner!\n".encode('utf-8'))
                    broadcast_game(game)
                    break
                else:
                    broadcast_game(game)
            else:
                conn.sendall("Invalid move. Try again.\n".encode('utf-8'))
        except ValueError:
            conn.sendall("Invalid input format. Please enter your move as 'row col'.\n".encode('utf-8'))

    conn.close()


def broadcast_game(game):
    # Broadcast the updated game state to both players
    for conn in clients:
        conn.sendall(f"Game Board:\n{game}\n".encode('utf-8'))


def startServer(port):
    game = TicTacToe.play(p1, p2)
    game.reset_game()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, port))
    server_socket.listen(2)
    print(f"Server started on port {port}. Waiting for players to connect...")

    global clients
    clients = []

    # Accept player 1
    player1, addr1 = server_socket.accept()
    print(f"Player 1 connected from {addr1}")
    clients.append(player1)
    player1_id = 0

    # Accept player 2
    player2, addr2 = server_socket.accept()
    print(f"Player 2 connected from {addr2}")
    clients.append(player2)
    player2_id = 1

    server_socket.close()
    print("Game over. Connections closed.")


if __name__ == "__main__":
    start_server(2000)
