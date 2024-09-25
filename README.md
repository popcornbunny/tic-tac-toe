# tic-tac-toe

This is the code for Computer Networks Project 1<br/>
Contributors: Katelyn Hanft, Faith Wilson, Alexa Hoover

The Rubric is as follows:

## Programming Assignment 1 Grading Rubric <br/>
Code Formatting:<br/>
_______ is well commented and formatted<br/>
_______ is well structured and good naming<br/>
_______ has contributing coder(s) full name(s) at the top of the files.<br/>
<br/>
Functionality (each are worth 2 points):<br/>
_______ Able to connect between itself (e.g. Java w/ Java)<br/>
_______ Able to connect between all version (e.g. Java w/ C, Java w/ Python, etc)<br/>
_______ Able to send at least one move between the players (any one pairing of the game)<br/>
_______ Able to send at least one move between the players (any pairing of the game)<br/>
_______ Able to complete a game (any pairing of the game)<br/>
_______ Able to start a new game (any pairing of the game)<br/>
_______ Able to end the game (any pairing of the game)<br/>
_______ Useful UI prompts for input.<br/>
_______ Creates and saves a log of all the messages.<br/>
_______ Each log entry has the info: Player, move, IP From, IP<br/>

## Programming Assignment 1 – TCP Tic Tac Toe <br/>

You will be working in groups of three or a pair depending on number of students in the course. For this project you will be creating a tic tac toe game that can be played over a network using TCP as the transport layer communication protocol. Your group will develop potentially three different versions of the game: Java, C, and Python (groups of two will only have two out of the three versions). However, each version will be able to connect and play with any of the other versions in your group.

As this class is supposed to focus on network programming the core of the game has already been written in Java, C, or Python and posted to D2L. You must use the core provided, if you get stuck on some aspect of it, or some part of it does not appear to be working correctly please contact me. I did do testing of each version and even wrote some JUnit tests for the Java version, but that does not mean I missed something.

Each version of the game will act as both a client (be able to connect to a server) and a server (be able to accept a connection). How you have two games connect will be up to your group.

### Details
Each version of the game will need an interface that allows a player to connect to another player to start a game. This can be done all with a text interface and while it just needs to be functional, prompts are required that help guide what the user needs to type in or do.

Once connected the ‘X’ player should have a way to input in the first move. After each move both players should see the updated board. After the board is displayed then the player who’s move next gets to go. When the game is over (win/loose/tie) a message should be displayed to each player letting them know if they won/lost/tied the game. Note that a lot of this is already provided in the core code.

Once the game is over the players should have the option to play again or disconnect. Again, there is already initial code provided to reset the game.

While the game is running each game should create and save a log file of all the messages sent and received. It should record which player is sending the message, what the action was (e.g. ‘X” at 1, 1), the IP address for where the message is from, and IP address of where the message is being sent.

### Group Version Control
Coordinating time between group members may be a challenge. I strongly encourage using Git or simply a shared Google Drive folder where you keep the most updated version of your code so your other group members can access it easily. That way if a member of your group wants to access your code while you are asleep, in class, at work, etc they can easily do so.

Important Note: It is your job to inform me (via email, office hours, etc…) if your partner(s) is not working with you on the project by not communicating, not showing up to work on it with you, or not providing any code when expected. Unless I am informed, I will automatically assume whatever work was turned in was done as a part of a collaborative effort.

Turning-In: A hard copy of your code to the correct Assignments folder of D2L (each group member will only turn in a copy of their server and client). In the comments for each file where you should put the author, be sure and note who worked on it. That way if the whole group worked on all the pieces, I can compute the grade accordingly. Additionally, each group demo their code on the Thursday in class after the due date.

### Extra Resources
I have links/resources listed below for threading in Java (normally covered in SWE 200) and C (normally covered in CMPE 320).

Java: http://docs.oracle.com/javase/tutorial/essential/concurrency/runthread.html

C: http://www.thegeekstuff.com/2012/04/create-threads-in-linux/

Python: https://realpython.com/python-sockets/

A Practical Guide to Python Threading By Examples: https://www.pythontutorial.net/python-concurrency/python-threading/#:~:text=Summary%201%20Use%20the%20Python%20threading%20module%20to,Only%20use%20threading%20for%20I%2FO%20bound%20processing%20applications.

### IMPORTANT NOTES

In C threads are much more operating system dependent. Python doesn't do threads in the way C and Java do (least the older versions didn't), you'll need to rely on what is built into the python sockets. Reminder that char in C is 8 bits, a char in Java is 16 bits (but a byte is only 8 bits), a char in python can vary in size.

# Due on Oct 23, 2024 10:00 PM
