import string
import sys
import os
import time
import argparse

#var inits
board_size = None
DARK = 9
LIGHT = 7
EMPTY = 0
board = []
PLAYER = None
OPPONENT = None



#argument parsing
def parse():
    global board_size
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', action = 'store_true', help = "this decides whether the player uses light or dark pieces")
    parser.add_argument('-n', type = int, help = "the size of the game board. Default is 11x11")
    args = parser.parse_args()

    board_size = args.n
    if board_size == None:
        board_size = 11
    if board_size < 5:
        exit(1, "Must use board at least 5x5 in size")
    if args.l:
        PLAYER = 7
        OPPONENT = 9
    else:
        OPPONENT = 7
        PLAYER = 9


def print_board():
    sys.stdout.write("  ")
    i = 0
    for c in string.ascii_lowercase:
      i += 1
      if i > board_size:
        break
      sys.stdout.write("   %s" % c)
    sys.stdout.write("\n   +")
    for i in range(0, board_size):
      sys.stdout.write("---+")
    sys.stdout.write("\n")

    for i in range(0, board_size):
      sys.stdout.write("%2d |" % (i + 1))
      for j in range(0, board_size):
        if board[i][j] == LIGHT:
          sys.stdout.write(" L |")
        elif board[i][j] == DARK:
          sys.stdout.write(" D |")
        else:
          sys.stdout.write("   |")
      sys.stdout.write("\n   +")
      for j in range(0, board_size):
        sys.stdout.write("---+")
      sys.stdout.write("\n")

def makeBoard(board_size):
    global EMPTY
    for i in range(0, board_size):
        row = []
        for j in range(0, board_size):
            row.append(EMPTY)
        board.append(row)

def main():
    global EMPTY
    parse()
    makeBoard(board_size)
    print_board()

main()