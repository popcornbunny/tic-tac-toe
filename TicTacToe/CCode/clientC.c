//
// Author Alexa Hoover,
//  Faith Wilson
//  TicTacToe Client
//
#include <stdio.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <string.h>
#include <stdlib.h>
#define BUFFER_SIZE 1024
#define MAX_LINE_LENGTH 1024

int read_line(int sockfd, char *buffer, int max_length) {
    int bytes_read = 0;
    char c;

    while (bytes_read < max_length - 1) {
        int result = recv(sockfd, &c, 1, 0);

        if (result <= 0) {
            // Error or connection closed
            return result;
        }

        buffer[bytes_read++] = c;

        if (c == '\n') {
            break;
        }
    }

    buffer[bytes_read] = '\0';
    return bytes_read;
}



void handle_game(int sockfd) {
    char buffer[BUFFER_SIZE];
    char sendBuffer[BUFFER_SIZE];
    int row, col;
    //read a line from the server
    int bytes_read;


    while (1) {
        memset(buffer, 0, sizeof(buffer));
        memset(sendBuffer, 0, sizeof(sendBuffer));
        //read messages
        while ((bytes_read = read_line(sockfd, buffer, MAX_LINE_LENGTH)) > 0) {
            printf("Received: %s", buffer);
            break; //bread out of the read to see if we need to do anything
        }
        //for each line from the server, check to see what to do

        if (strstr(buffer, "wins") != NULL || strstr(buffer, "disconnected") != NULL) {
            break; // Exit loop if the game is over
        }
        if (strstr(buffer, "Enter your move") != NULL) {
            printf("Enter your move (row col): ");

            if (fgets(sendBuffer, sizeof(sendBuffer), stdin) != NULL) {
                printf("You entered: %s", sendBuffer);
            } else {
                printf("Error reading input.");
            }
            write(sockfd, sendBuffer, strlen(sendBuffer));
        }
    }
}
int main() {

    int sockfd;
    struct sockaddr_in server_addr;

    // Create socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }
    // Specify server address
    memset(&server_addr, '\0', sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(3000); // Replace with your server port
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // Change to>
    // Connect to the server
    int connfd;
    connfd = connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr));
    if (connfd < 0)
    {
        close(sockfd);
        exit(EXIT_FAILURE);
    }

// Handle game loop
    handle_game(sockfd);
// Close socket
    close(sockfd);
    return 0;
}