/**
 * author Faith Wilson
 * Tic-Tac-Toe Client
 */

import java.io.*;
import java.net.Socket;
import java.util.Scanner;

public class Client {
    public void client(String ip, int port) throws Exception {
        final String SERVER_ADDRESS = ip;
        final int PORT = port;
        System.out.println("Connecting to the Tic-Tac-Toe server...");
        Socket socket = new Socket(SERVER_ADDRESS, PORT);
        System.out.println("Connected to server at " + SERVER_ADDRESS + " on port " + PORT);

        BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        BufferedWriter output = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
        BufferedReader userInput = new BufferedReader(new InputStreamReader(System.in));

        String serverMessage;

        while ((serverMessage = input.readLine()) != null) {
            System.out.println(serverMessage);  // Display the message from the server

            // If the message contains "win" or "draw", the game is over
            if (serverMessage.contains("win") || serverMessage.contains("draw")) {
                System.out.println("\nGame over. Closing connection.");
                break;
            }

            // When asked to move read in input
            if (serverMessage.contains("Enter your move (row col):")) {
                String move = userInput.readLine();

                // write move to server
                output.write(move);
                output.newLine();
                output.flush();
            }

        }
    }


    public static void main(String[] args) throws Exception {
        Client client = new Client();
        Scanner scan = new Scanner(System.in);
        System.out.print("Enter the ip you want to connect to : ");
        String ipAddress = scan.nextLine();
        System.out.print("Enter your port number : ");
        int portNum = scan.nextInt();

        client.client(ipAddress,portNum);
    }
}