// Alexa Hoover C version, Computer Networking 10/23/24

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
        printf("\n Socket creation error \n");
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(8080);

    if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }

    // Connect to server
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        printf("\nConnection Failed \n");
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

            // Receive message from the server
            memset(buffer, 0, sizeof(buffer));
            int bytes_read = read(sock, buffer, sizeof(buffer));
            if (bytes_read <= 0) {
                printf("Server disconnected.\n");
                close(sock);
                return 0;
            }

            printf("Server response:\n%s\n", buffer);
            logMessage(buffer);

            if (strstr(buffer, "WIN") != NULL) {
                printf("Player %c wins!\n", buffer[4]); // buffer[4] will be the winner ('X' or 'O')
                break;
            } else if (strstr(buffer, "TIE") != NULL) {
                printf("It's a tie!\n");
                break;
            } else if (strstr(buffer, "INVALID") != NULL) {
                printf("Invalid move! Try again.\n");
            }
        }

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

    // Message log (DONES'T WORK)
    printf("\nMessage Log:\n%s\n", messageLog);

    close(sock);
    return 0;
}
