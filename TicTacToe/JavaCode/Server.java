import java.io.*;
import java.net.*;

public class Server {
    private TicTacToe game;

    public Server() {
        game = new TicTacToe();
        game.resetGame();
    }

    public void serverStart(int port) throws IOException {

        {

            ServerSocket ss = new ServerSocket(port);    // Create server Socket
            //written to server
            Socket player1 = ss.accept(); // connect it to client socket
            System.out.println("player1 Connected");
            Socket player2 = ss.accept();
            System.out.print("player2 Connected");


            PrintStream psPlayer1 = new PrintStream(player1.getOutputStream());
            // to send data to the client

            BufferedReader bufferPlayer1 = new BufferedReader(new InputStreamReader(player1.getInputStream()));
            // to read data coming from the client

            PrintStream psPlayer2 = new PrintStream(player2.getOutputStream());
            // to send data to the client2

            BufferedReader bufferPlayer2 = new BufferedReader(new InputStreamReader(player2.getInputStream()));
            // to read data coming from the client2

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
                psCurrent.println("It is your turn Player " + currentPlayer );
                psCurrent.println("Enter your move (row col):");

                String move = bufferCurrent.readLine();
                String moveRaC[] = move.split(" "); //parse by a space
                int row = Integer.parseInt(moveRaC[0]);
                int col = Integer.parseInt(moveRaC[1]);

                game.setPlayer(currentPlayer); // set players in game

                if (game.makeMove(row, col)) { //if a valid move
                    if (game.checkForWin()) {   //if you win close the game
                        psCurrent.println("You are the Winner");
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
            player1.close();
            player2.close();
            ss.close();

            System.out.println("Game over. Connections closed.");
            // end of while
        }
    }
    public static void main (String[]args) throws IOException {
        Server server = new Server();
        server.serverStart(2000);

    }
}

