//Alexa Hoover Computer Networks 10/23/24

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>

char messageLog[1024 * 10] = "";

void logMessage(const char *message) {
    strcat(messageLog, message);
    strcat(messageLog, "\n");
}

int main() {
    int sock = 0;
    struct sockaddr_in serv_addr;
    char buffer[1024] = {0};
    int row, col;
    char replay_choice[10];
    int replay = 1;

    // Create client socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Socket creation error");
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(8080);

    if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) {
        perror("Invalid address/Address not supported");
        return -1;
    }

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Connection Failed");
        return -1;
    }

    while (replay) {
        // Game loop
        while (1) {
            printf("Enter your move (row col): ");
            scanf("%d %d", &row, &col);

            // Send move to the server
            char move[100];
            snprintf(move, sizeof(move), "%d %d", row, col);
            send(sock, move, strlen(move), 0);
            logMessage(move);

            memset(buffer, 0, sizeof(buffer));
            read(sock, buffer, 1024);
            printf("Server response:\n%s\n", buffer);
            logMessage(buffer);

            if (strcmp(buffer, "WIN") == 0) {
                printf("You win!\n");
                logMessage("WIN");
                break;
            } else if (strcmp(buffer, "TIE") == 0) {
                printf("It's a tie!\n");
                logMessage("TIE");
                break;
            } else if (strcmp(buffer, "INVALID") == 0) {
                printf("Invalid move! Try again.\n");
                logMessage("INVALID");
            }
        }

        // Ask if the player wants to replay
        printf("Replay? (yes/no): ");
        scanf("%s", replay_choice);

        send(sock, replay_choice, strlen(replay_choice), 0);
        logMessage(replay_choice);

        if (strncmp(replay_choice, "yes", 3) == 0) {
            replay = 1;
        } else {
            replay = 0;
            break;
        }
    }

    printf("\nGame Over. Message Log:\n%s\n", messageLog);

    close(sock);
    return 0;
}
