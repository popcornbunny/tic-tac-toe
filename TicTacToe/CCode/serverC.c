//
// Author Alexa Hoover,
//  Faith Wilson
//  TicTacToe Server
//
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <arpa/inet.h>
#define PORT 3000
#define BUFFER_SIZE 1024
#define SIZE 3 // Tic-Tac-Toe board size
// TicTacToe struct definition


struct TicTacToe {
    char values[SIZE][SIZE]; // Game board
    int player_move; // -1 = game not started, 0 = 'O', 1 = 'X'
    int length; // Size of the board
};
// Function prototypes
void initializeBoard(struct TicTacToe *game_board);
void resetGame(struct TicTacToe *game_board);
int makeMove(struct TicTacToe *game_board, int r, int c, char marker);
int checkForWin(struct TicTacToe *game_board);
char* toString(struct TicTacToe *game_board);
void printBoard(struct TicTacToe *game_board, int client1, int client2);
void sendTurnMessage(int currentPlayer, int client1, int client2);
void sendMessage(int client, const char *message);

void printLine(const char *message) {
    printf(message);
    fflush(stdout);
}
void initializeBoard(struct TicTacToe *game_board) {
    game_board->length = SIZE;
    for (int r = 0; r < game_board->length; r++)
        for (int c = 0; c < game_board->length; c++)
            game_board->values[r][c] = ' ';
}

void resetGame(struct TicTacToe *game_board) {
    initializeBoard(game_board);
    game_board->player_move = -1;
}

int makeMove(struct TicTacToe *game_board, int r, int c, char marker) {
    if (game_board->values[r][c] == ' ') {
        game_board->values[r][c] = marker; // Use the marker passed to the function
        return 1; // Move successful
    }
    return 0; // Invalid move
}

int checkForWin(struct TicTacToe *game_board) {
    char win_token;
    // Determine the current player's marker
    if (game_board->player_move == 0) {
        win_token = 'O'; // Player 1 is 'O'
        printLine("zero");
    }
    else {
        win_token = 'X'; // Player 2 is 'X'
        printLine(("XPlayer"));
    }
    // Check rows
    for (int r = 0; r < game_board->length; r++) {
        if (game_board->values[r][0] == win_token &&
            game_board->values[r][1] == win_token &&
            game_board->values[r][2] == win_token)
            return 1; // Win
    }

    // Check columns
    for (int c = 0; c < game_board->length; c++) {
        if (game_board->values[0][c] == win_token &&
            game_board->values[1][c] == win_token &&
            game_board->values[2][c] == win_token)
            return 1; // Win
    }
    // Check diagonals
    if (game_board->values[0][0] == win_token &&
        game_board->values[1][1] == win_token &&
        game_board->values[2][2] == win_token)
        return 1; // Win
    if (game_board->values[0][2] == win_token &&
        game_board->values[1][1] == win_token &&
        game_board->values[2][0] == win_token)
        return 1; // Win
    return 0; // No win
}
char* toString(struct TicTacToe *game_board) {
    char *board = malloc(49 * sizeof(char));
    board[0] = '\0';
    strcat(board, "-------\n");
    for (int r = 0; r < game_board->length; r++) {
        for (int c = 0; c < game_board->length; c++) {
            strcat(board, "|");
            strncat(board, &game_board->values[r][c], 1);
        }
        strcat(board, "|\n");
        strcat(board, "-------\n");
    }
    return board;
}
void printBoard(struct TicTacToe *game_board, int client1, int client2) {
    char *board = toString(game_board);
    send(client1, board, strlen(board), 0);
    send(client2, board, strlen(board), 0);
    free(board);
}

void sendTurnMessage(int currentPlayer, int client1, int client2) {
    char message[BUFFER_SIZE];
    snprintf(message, sizeof(message), "Player %d's turn. Enter your move (row col): \n", currentPlayer + 1);
    printf(message);
    fflush(stdout);
    send(currentPlayer == 0 ? client1 : client2, message, strlen(message), 0);
}

void sendMessage(int client, const char *message) {
    send(client, message, strlen(message), 0);
}

int main() {
    int server_fd, client1, client2;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_len = sizeof(client_addr);
    char buffer[BUFFER_SIZE];
    struct TicTacToe *game = malloc(sizeof(struct TicTacToe));
    // Create socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }
    // Bind the socket
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    //server_addr.sin_addr.s_addr = inet_addr("192.168.86.217");
    server_addr.sin_port = htons(PORT);


    if (bind(server_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Bind failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }
    // Listen for connections
    listen(server_fd, 2);

    printf("Waiting for players to connect...\n");
    // Accept two players
    client1 = accept(server_fd, (struct sockaddr *)&client_addr, &addr_len);
    printf("Player 1 connected from %s\n", inet_ntoa(client_addr.sin_addr));
    client2 = accept(server_fd, (struct sockaddr *)&client_addr, &addr_len);
    printf("Player 2 connected from %s\n", inet_ntoa(client_addr.sin_addr));
    // Initialize game board
    resetGame(game);
    printBoard(game, client1, client2);
    int currentPlayer = 0; // 0 for Player 1 (O), 1 for Player 2 (X)
    while (1) {
        int row, col;
        sendTurnMessage(currentPlayer, client1, client2); // Notify player of their turn
        // Receive move from the current player
        ssize_t bytes_received = recv(currentPlayer == 0 ? client1 : client2, buffer, sizeof(buffer), 0);
        if (bytes_received <= 0) {
            snprintf(buffer, sizeof(buffer), "Player %d disconnected. Game over!\n", currentPlayer + 1);
            sendMessage(client1, buffer);
            sendMessage(client2, buffer);
            break;
        }
        sscanf(buffer, "%d %d", &row, &col);
        // Validate move
        if (makeMove(game, row, col, currentPlayer == 0 ? 'O' : 'X')) { // Pass the correct marker
            game->player_move = currentPlayer;
            printBoard(game, client1, client2);
            if (checkForWin(game)) {
                snprintf(buffer, sizeof(buffer), "Player %d wins!\n", currentPlayer + 1);
                sendMessage(client1, buffer);
                sendMessage(client2, buffer);
                break;
            }
            currentPlayer = (currentPlayer + 1) % 2; // Switch players
        }
        else {
            snprintf(buffer, sizeof(buffer), "Invalid move. Try again.\n");
            sendMessage(currentPlayer == 0 ? client1 : client2, buffer);
        }
    }
    // Close sockets
    close(client1);
    close(client2);
    close(server_fd);
    free(game);
    printf("Game over. Connections closed.\n");
    return 0;
}
