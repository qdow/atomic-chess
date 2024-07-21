# Atomic Chess

## Table of Contents
1. [Introduction](#introduction)
2. [How To Play](#how-to-play)

## Introduction
In this variety of chess, when pieces are captured, they cause an explosion that blows up every piece 
on the squares surrounding the captured piece including the piece that did the capturing. 
Pawns on the squares surrounding the capturing/captured piece are the only pieces that survive 
the explosion. Players can end up blowing up their own pieces.

Because of the explosive nature of captures, kings are not allowed to make captures, and the game 
can be ended by a player capturing a piece that would cause the opponent's king to blow up in the 
resulting explosion, however a move cannot be made if it would blow up both kings at the same time. 
This makes for interesting and unique gameplay compared to regular chess! 

For more information on the atomic variety of chess, please see [this page](https://www.chess.com/terms/atomic-chess)
from Chess.com.

Enjoy! :)


## How to play
After downloading the game files, open a terminal window into the directory in which the files were saved.
The game can be run by using ` python main.py `

White pieces start on the bottom half of the board and white player goes first.
On your turn, type the algebraic notation of the square of the piece you want to move when asked 
"where you would like to move 'From:', then type the algebraic notation of the square you would like 
to move to.

For example, the first turn of the game could go like this:

`From: g2`  
`To: g4`

If a move is not valid, the board will not update and it will prompt you again.

After every turn, the board will update and it will be the next player's turn to move.
Once the game is won, the winner will be announced and you will be prompted to play again or type 'q' to quit.

Thanks for playing!