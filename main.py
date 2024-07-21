#!/usr/bin/env python3
"""
Filename: main.py
Author:
Date updated: 2024-07-09
Description: Uses GameBoard.py and GamePiece.py to play the "atomic" variety of chess
"""

from GamePiece import *
from GameBoard import *

if __name__ == '__main__':
    print("Welcome to Atomic Chess!\n")
    print(("In this variety of chess, when pieces are captured, they cause an explosion that blows up every piece "
           "on the squares surrounding the captured piece including the piece that did the capturing. "
           "Pawns on the squares surrounding the capturing/captured piece are the only pieces that survive "
           "the explosion. Players can end up blowing up their own pieces.\n"
           "Because of the explosive nature of captures, kings are not allowed to make captures, and the game "
           "can be ended by a player capturing a piece that would cause the opponent's king to blow up in the "
           "resulting explosion, however a move cannot be made if it would blow up both kings at the same time. "
           "This makes for interesting and unique gameplay compared to regular chess! Enjoy! :)\n"))
    print(("How to play:\nWhite pieces start on the bottom half of the board and white player goes first.\n"
           "On your turn, type the algebraic notation of the square of the piece you want to move when asked "
           "where you would like to move 'From:', then type the algebraic notation of the square you would like "
           "to move to.\nFor example, the first turn of the game could go like this:"))
    print("     From: g2\n     To: g4")
    print("If a move is not valid, the board will not update and it will prompt you again.\n")

    play = input("Type any key to play or 'q' to quit: ")

    while play.lower() != "q":
        game = GameBoard()
        game.play_game()
        play = input("Type any key to play again or 'q' to quit: ")

    print("\nThanks for playing!")
