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
        ss = new ServerSocket(port);    // Create server Socket
        player1 = ss.accept(); // Connect to player 1
        System.out.println("player1 Connected from " + player1.getInetAddress());
        player2 = ss.accept(); // Connect to player 2
        System.out.println("player2 Connected from " + player2.getInetAddress());

        psPlayer1 = new PrintStream(player1.getOutputStream(), true); // true = autoflush
        bufferPlayer1 = new BufferedReader(new InputStreamReader(player1.getInputStream()));

        psPlayer2 = new PrintStream(player2.getOutputStream(), true); // true = autoflush
        bufferPlayer2 = new BufferedReader(new InputStreamReader(player2.getInputStream()));
    }

    // Method to log moves and send the log to both players
    private void logMove(int player, int row, int col, String ip, String ip2) {
        String logEntry = ("Current player " + player + " ip: " + ip + " made a move at row " + row + ", col " + col + " against " + ip2);
        // Send log to both players
        psPlayer1.println(logEntry);
        psPlayer2.println(logEntry);
        System.out.println(logEntry); // Also log it to the server console
    }

    public void serverStart() throws IOException {
        int currentPlayer = 0;
        boolean runningGame = true;

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

            // Send messages to the current player
            psCurrent.println("Player 0: 0       Player 1 : X \n");
            psCurrent.println("It is your turn Player " + currentPlayer);
            psCurrent.println("Enter your move (row col):");
            psCurrent.flush(); // Force output to be sent

            System.out.println("Waiting for Player " + currentPlayer + " to make a move...");

            String move = bufferCurrent.readLine();
            System.out.println("Player " + currentPlayer + " entered move: " + move);

            String[] moveRaC = move.split(" "); // Parse by a space
            int row = Integer.parseInt(moveRaC[0]);
            int col = Integer.parseInt(moveRaC[1]);

            game.setPlayer(currentPlayer); // Set players in game

            if (game.makeMove(row, col)) { // If a valid move
                InetAddress ip1 = player1.getInetAddress();
                InetAddress ip2 = player2.getInetAddress();

                logMove(currentPlayer, row, col, ip1.getHostAddress(), ip2.getHostAddress());

                if (game.checkForWin()) {
                    psCurrent.println("You are the Winner");
                    if (currentPlayer == 0) {
                        psPlayer2.println("You have lost");
                    } else {
                        psPlayer1.println("You have lost");
                    }
                    runningGame = false;
                } else {
                    currentPlayer = (currentPlayer == 0) ? 1 : 0; // Switch players
                }
            } else {
                psCurrent.println("Invalid move");
            }

            psPlayer1.println(game); // Print the gameboard to player 0
            psPlayer2.println(game); // Print the gameboard to player 1
            psCurrent.flush(); // Force output to be sent
        }
        psPlayer1.println("\n *A new Game is Beginning*");
        psPlayer2.println("\n *A new Game is Beginning*");
        game.resetGame(); // Restart board
        serverStart(); // Start Again


        // Close connections after the game ends
        player1.close();
        player2.close();
        ss.close();

        System.out.println("\nGame over. Connections closed.");
    }

    public static void main(String[] args) throws IOException {
        Server server = new Server(2000);
        server.serverStart();
    }
}
