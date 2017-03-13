import string
import sys
import os
import time
import argparse
import random

#consts
DARK = 9
LIGHT = 7
EMPTY = 0

#var inits
board_size = None
board = []
PLAYER = None
OPPONENT = None
curr_turn = None
ROOT = None
choice = None
nextmove = None

#class defs
class Node:
    def __init__(self):
        self.position = []
        self.heuristic = -9999
        self.children = None #array of nodes
        self.total_heuristic = None


#funcition defs
#argument parsing
def parse():
    global board_size
    global curr_turn
    global PLAYER
    global OPPONENT

    parser = argparse.ArgumentParser()

    parser.add_argument('-l', action = 'store_true', help = "this decides whether the player uses light or dark pieces")
    parser.add_argument('-n', type = int, help = "the size of the game board. Default is 11x11")
    args = parser.parse_args()

    board_size = args.n
    if board_size == None:
        board_size = 11
    if board_size < 5 or board_size >26:
        exit(1, "Must use board between 5 and 26 in size")
    if args.l:
        PLAYER = 7
        OPPONENT = 9
        curr_turn = PLAYER
    else:
        OPPONENT = 7
        PLAYER = 9
        curr_turn = OPPONENT


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


def is_empty(column, row):
    if board[row][column] == EMPTY:
        return True
    else:
        return False

#computer's move
def rand_move():
    column = random.randint(0, board_size-1)
    row = random.randint(0, board_size-1)
    correct_move = is_empty(column, row)
    while not correct_move:
        column = random.randint(0, board_size-1)
        row = random.randint(0, board_size-1)
        correct_move = is_empty(column, row)
    board[row][column] = curr_turn

#read player's move
def read_move():
    move = raw_input("Enter move: \n")
    column = ord(move[0]) - 97
    row = int(move[1:])-1
    while not is_empty(column, row):
        move = raw_input("Incorrect move. Try again\n")
        column = ord(move[0]) - 97
        row = int(move[1:]) - 1
    board[row][column] = curr_turn


def minimax(node):
    global choice
    maxtotal = -99999
    for child in range(0, len(node.children)):
        curr = node.children[child]
        submax = curr.children[0]
        for subchild in range(0, len(curr.children)):
            if curr.children[subchild].heuristic > submax.heuristic:
                submax = curr.children[subchild]
        curr.total_heuristic = submax.heuristic - curr.heuristic
        if curr.total_heuristic > maxtotal:
            maxtotal = curr.total_heuristic
            choice = curr
    total_move_value = node.heuristic - maxtotal
    return total_move_value


def next_move(possible_moves):
    moves = {}
    for move in possible_moves:
        cost = minimax(move)
        moves[move] = cost
    max = -999999
    best_move = None
    for key, value in moves.iteritems():
        if value>max:
            best_move = key
            max = value
    return best_move





def evaluateBoard(board):

def findPossibleMoves():
    for i in range(0, board_size):
        for j in range(0, board_size):
            if is_empty(i, j):



#calculate heuristics
#determine possible moves

def main():
    global EMPTY
    global curr_turn
    parse()
    makeBoard(board_size)
    print_board()
    while True:
        if curr_turn == PLAYER:
            rand_move()
            print_board()
            curr_turn = OPPONENT
        if curr_turn == OPPONENT:
            read_move()
            print_board()
            curr_turn = PLAYER

main()