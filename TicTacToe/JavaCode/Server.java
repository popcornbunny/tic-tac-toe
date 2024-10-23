/**
 * author Faith Wilson
 * Tic-Tac-Toe Server
 */

import java.io.*;
import java.net.*;

public class Server {
    private TicTacToe game;
    private Socket player1;
    private Socket player2;
    private PrintStream psPlayer1;
    private PrintStream psPlayer2;
    private BufferedReader bufferPlayer1;
    private BufferedReader bufferPlayer2;
    private ServerSocket ss;
    public Server(int port) throws IOException {
        game = new TicTacToe();
        game.resetGame();
        ServerSocket ss = new ServerSocket(port);    // Create server Socket
        //written to server
        player1 = ss.accept(); // connect it to client socket
        System.out.println("player1 Connected");
        player2 = ss.accept();
        System.out.print("player2 Connected");


         psPlayer1 = new PrintStream(player1.getOutputStream());
        // to send data to the client

         bufferPlayer1 = new BufferedReader(new InputStreamReader(player1.getInputStream()));
        // to read data coming from the client

         psPlayer2 = new PrintStream(player2.getOutputStream());
        // to send data to the client2

         bufferPlayer2 = new BufferedReader(new InputStreamReader(player2.getInputStream()));
        // to read data coming from the client2
    }

    public void serverStart() throws IOException {

        {
            int currentPlayer = 0;
            boolean runningGame = true;

            // server executes continuously until game is determined false
            while (runningGame) {
                PrintStream psCurrent;
                BufferedReader bufferCurrent;

                // Determine the current player
                if (currentPlayer == 0) {
                    psCurrent = psPlayer1;
                    bufferCurrent = bufferPlayer1;
                } else {
                    psCurrent = psPlayer2;
                    bufferCurrent = bufferPlayer2;
                }
                //Written to CLIENT
                psCurrent.println("Player 0: 0       Player 1 : X \n");
                psCurrent.println("It is your turn Player " + currentPlayer);
                psCurrent.println("Enter your move (row col):");

                String move = bufferCurrent.readLine();
                String moveRaC[] = move.split(" "); //parse by a space
                int row = Integer.parseInt(moveRaC[0]);
                int col = Integer.parseInt(moveRaC[1]);

                game.setPlayer(currentPlayer); // set players in game

                if (game.makeMove(row, col)) { //if a valid move
                    if (game.checkForWin()) {   //if you win close the game
                        psCurrent.println("You are the Winner");
                        if (currentPlayer == 0) { // Depending on which player is up switch
                            psCurrent = psPlayer2;
                        } else {
                            psCurrent = psPlayer1;
                        }
                        psCurrent.println("You have lost"); //print to the other player
                        runningGame = false;
                    } else {
                        currentPlayer = (currentPlayer == 0) ? 1 : 0; //change which player in being read from
                    }
                } else {
                    psCurrent.println("Invalid move");
                }
                psPlayer1.println(game); //print the gameboard to player 0
                psPlayer2.println(game); //print the gameboard to player 1

            }
            psPlayer1.println("\n *A new Game is Beginning*"); //print the gameboard to player 0
            psPlayer2.println("\n *A new Game is Beginning*"); //print the gameboard to player 1
            game.resetGame(); // Restart board
            serverStart(); // Start Again
            }
            player1.close();
            player2.close();
            ss.close();

            System.out.println("\nGame over. Connections closed.");
            // end of while
        }

    public static void main (String[]args) throws IOException {
        Server server = new Server(2000);
        server.serverStart();
    }
}
