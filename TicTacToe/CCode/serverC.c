#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>
#include "TicTacToe.c"

#define PORT 8080
#define BUFFER_SIZE 1024

struct Connection {
    int socket;
    struct TicTacToe *game;
    char player;
};

void *handle_client(void *arg) {
    struct Connection *conn = (struct Connection *)arg;
    int sock = conn->socket;
    struct TicTacToe *game = conn->game;

    char buffer[BUFFER_SIZE];
    int move_r, move_c;

    while (1) {
        if (recv(sock, buffer, sizeof(buffer), 0) <= 0) {
            break;
        }

        sscanf(buffer, "%d %d", &move_r, &move_c);
        if (makeMove(game, move_r, move_c)) {
            char *board = toString(game);
            send(sock, board, strlen(board), 0);
            free(board);

            if (checkForWin(game)) {
                snprintf(buffer, sizeof(buffer), "Player %c wins!\n", conn->player);
                send(sock, buffer, strlen(buffer), 0);
                break;
            }
        } else {
            snprintf(buffer, sizeof(buffer), "Invalid move. Try again.\n");
            send(sock, buffer, strlen(buffer), 0);
        }
    }

    close(sock);
    free(conn);
    return NULL;
}

int server_main(int argc, char **argv) {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);

    struct TicTacToe *game = malloc(sizeof(struct TicTacToe));
    resetGame(game);
    setPlayer(game, 0);

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Socket failed");
        exit(EXIT_FAILURE);
    }

    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 3) < 0) {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }

    printf("Waiting for players to connect...\n");

    while (1) {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            perror("Accept failed");
            continue;
        }

        struct Connection *conn = malloc(sizeof(struct Connection));
        conn->socket = new_socket;
        conn->game = game;
        conn->player = 'X';

        pthread_t thread_id;
        pthread_create(&thread_id, NULL, handle_client, conn);
    }

    close(server_fd);
    free(game);
    return 0;
}
