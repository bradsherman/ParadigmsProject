Paradigms Final Project
=======================

Brad Sherman & Ben Dalgarn
--------------------------

This project is a multi-player game that utilizes the python PyGame and Twisted
libraries. The objective of the game is to protect the blocks behind your player
from the ball floating around on the screen. It is a spin-off from the classic
brick-breaker game.

To Play the Game
----------------
First, designate a host (player1) and a client (player2). We have provided a few
test script to aid in the process of getting the players set up. The host can
run `python src/get_ip.py` to have their ip displayed to the screen and then the client
can modify `src/client.py` line 11 to contain the correct ip address. Also,
player1 can run `src/replace_ip.sh` which will get their ip and automatically
replace it in `src/client.py`. Then player1 simply needs to push the changes to
`src/client.py` and player2 needs to pull those changes down, then the programs
should be ready to connect. After that, player1 needs to run the command
`./player1.py` first to start the server. Once that has happened, player2 can run
`./player2.py` to connect. Then the game screens will pop up. Player1 moves by
pressing the right and left arrow keys, and player2 moves by pressing the 'a'
and 'd' keys. Once one player quits, the screen will let each player know, and
then the player should press enter to close the window.

**Note**: This assumes each computer has an installation of python2.7 in
/usr/bin/

How it Works
------------
This game works just like the classic single player brick-breaker game, except
now you can play your friends! It is a real time system so each player
experiences the same game even if they are not together!
