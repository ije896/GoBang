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
valid_neighbor_distance = 1

# run calculation const
INVALID = -42
dirs = ["left", "up-left", "up", "up-right", "right", "down-right", "down", "down-left"]

#var inits
board_size = None
board = []
PLAYER = None
OPPONENT = None
curr_turn = None
ROOT = None
choice = None
nextmove = None
numTurns = 0

#class defs
class Node:
    def __init__(self, x, y):
        self.position = (x, y) #tuples are immutable
        self.heuristic = -9999
        self.children = None #array of nodes of proceeding possible moves
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
        PLAYER = DARK
        OPPONENT = LIGHT
        curr_turn = PLAYER
    else:
        OPPONENT = DARK
        PLAYER = LIGHT
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
    move_played = str(unichr(column + 97)) + str(row + 1)
    sys.stdout.flush()
    print_board()
    print "Move played:", move_played
    sys.stdout.flush()

#read player's move
#TODO: check for incorrect inputs
def read_move():
    move = raw_input("Enter move: ")
    column = ord(move[0]) - 97
    row = int(move[1:])-1
    while not is_empty(column, row) or column>=board_size or row>=board_size:
        move = raw_input("Incorrect move. Try again: ")
        column = ord(move[0]) - 97
        row = int(move[1:]) - 1
    board[row][column] = curr_turn
    print_board()
    sys.stdout.flush()
    print "Move played:",move
    sys.stdout.flush()


def minimax(node):
    global choice
    #calulate heuristics for game tree of depth 2
    row = node.position[0]
    col = node.position[1]
    board[row][col] = PLAYER
    node.heuristic = calculate_runs_value(PLAYER)
    #print "calculate_runs_value(PLAYER): ", calculate_runs_value(PLAYER)
    node.children = findPossibleMoves()

    for child in range(len(node.children)):
        ch_row = node.children[child].position[0]
        ch_col = node.children[child].position[1]
        board[ch_row][ch_col] = OPPONENT
        node.children[child].heuristic = calculate_runs_value(OPPONENT)
        """
        node.children[child].children = findPossibleMoves()

        for subchild in range(len(node.children[child].children)):
            subch_row = node.children[child].children[subchild].position[0]
            subch_col = node.children[child].children[subchild].position[1]
            board[subch_row][subch_col] = PLAYER
            node.children[child].children[subchild].heuristic = calculate_runs_value(PLAYER)
            board[subch_row][subch_col] = EMPTY
            """
        board[ch_row][ch_col] = EMPTY
    board[row][col] = EMPTY
    """
    opp_max = 999999
    temp = 0

    for child_ndx in range(0, len(node.children)):
        curr = node.children[child_ndx]

        for depth2_ndx in range(0, len(curr.children)):
            temp = -1 * curr.heuristic
            temp = temp + curr.children[depth2_ndx].heuristic

            if (temp < opp_max):
                opp_max = temp
    node.total_heuristic = node.heuristic + opp_max
    return node.total_heuristic
    """
    child_sum = 0
    for index in range(0, len(node.children)):
        curr = node.children[index]
        child_sum+= curr.heuristic
    node.total_heuristic = node.heuristic - child_sum
    return node.total_heuristic



def next_move():
    global PLAYER
    global numTurns
    global curr_turn
    #if PLAYER == LIGHT
    #print
    if numTurns == 0:
        row = board_size/2
        col = board_size/2
        board[row][col] = curr_turn
        move_played = str(unichr(col + 97)) + str(row + 1)
        sys.stdout.flush()
        print "Move played:",move_played
        sys.stdout.flush()
    else:
        moves = {}
        possible_moves = findPossibleMoves()
        for move in possible_moves:
            cost = minimax(move)
            moves[move.position] = cost
        max = -99999999999999
        best_move = None
        for key, value in moves.iteritems():
            if value>max:
                best_move = key
                max = value
        row = best_move[0]
        col = best_move[1]
        board[row][col] = curr_turn
        move_played = str(unichr(col+97)) + str(row+1)
        print_board()
        sys.stdout.flush()
        print "Move played:",move_played
        sys.stdout.flush()


def findPossibleMoves():
    #find empty squares,
    #create node for them
    #add them to the list
    #create lower admissibility for addition to list
    possible_moves = []
    global valid_neighbor_distance
    for i in range(0, board_size):
        for j in range(0, board_size):
            if is_empty(j, i):
                node = Node(i, j)
                possible_moves.append(node)
    to_del = []
    for i in range(len(possible_moves)):
        curr = possible_moves[i]
        if (no_neighbors_within_n(curr, valid_neighbor_distance)):
            to_del.append(i)
    # do deletions
    num_del = 0
    for i in range(len(to_del)):
        del possible_moves[to_del[i] - num_del]
        num_del += 1

    return possible_moves

def no_neighbors_within_n(node, n):
    row = node.position[0]
    col = node.position[1]
    for i in range(-1*n, n+1):
        for j in range(-1*n, n+1):
            if (0<=row+i and row+i<board_size) and (0<=col+j and col+j<board_size):
                if not is_empty(col+j, row+i):
                    return False
    return True


#returns heuristic for 1 player for a given board
def calculate_runs_value(me):
   run_weights = {}
   player = 0
   if (me == PLAYER):
       player = PLAYER
       run_weights[2] = 1
       run_weights[3] = 10000
       run_weights[4] = 100000
       #run_weights[30] = 10000000
       for x in range(5, 25):
           run_weights[x] = 1000000
   else:
       player = OPPONENT
       run_weights[2] = 1
       run_weights[3] = 100000
       run_weights[4] = 1000000
       #run_weights[30] = 10000000
       for x in range(5, 25):
           run_weights[x] = 10000000



    #potentially make global var
   player_positions = []
   # iterate over board to find player positions
   for i in range(board_size):
       for j in range(board_size):
           if (board[i][j] == player):
               player_positions.append([i,j])

   # iterate over player positions
   # for each position go in the 8 directions and check if there is a run
   runs = []
   for i in range(len(player_positions)):
       curr_pos = player_positions[i]
       curr_runs = calculate_runs(curr_pos, player)

       for run in curr_runs:
           runs.append(run)

   #return runs
   h = 0
   for run in runs:
       h = h + run_weights[len(run)]

   return h


#pos[0] = row, pos[1] = col
def calculate_runs(pos, player):
   runs = []
   for dir in dirs:
       curr_pos = pos
       curr_run = []
       curr_run.append(pos)

       while (True):
           n_pos = next_pos(curr_pos, dir)
           if (n_pos == INVALID):
               break
           if (board[n_pos[0]][n_pos[1]] == player):
               curr_run.append(n_pos)
               curr_pos = n_pos
           else:
               break

       if (len(curr_run) > 1):
           runs.append(curr_run)

   return runs

def next_pos(pos, dir):
   n_pos = [0,0]
   if (dir == "left"):
       n_pos = [pos[0],pos[1]-1]
   elif (dir == "up-left"):
       n_pos = [pos[0]-1, pos[1]-1]
   elif (dir == "up"):
       n_pos = [pos[0]-1, pos[1]]
   elif (dir == "up-right"):
       n_pos = [pos[0]-1, pos[1]+1]
   elif (dir == "right"):
       n_pos = [pos[0], pos[1]+1]
   elif (dir == "down-right"):
       n_pos = [pos[0]+1, pos[1]+1]
   elif (dir == "down"):
       n_pos = [pos[0]+1, pos[1]]
   elif (dir == "down-left"):
       n_pos = [pos[0]+1, pos[1]-1]

   if not ((0 <= n_pos[0] and n_pos[0] <= board_size-1) and (0 <= n_pos[1] and n_pos[1] <= board_size-1)):
       n_pos = INVALID

   return n_pos

def is_over():
    if numTurns == board_size * board_size:
        sys.stdout.flush()
        print "Draw!"
        sys.stdout.flush()
        return True
    return False



def main():
    global EMPTY
    global curr_turn
    global numTurns
    parse()
    makeBoard(board_size)
    print_board()
    while not is_over(): #while game is in play
        if curr_turn == PLAYER:
            """possible_moves = findPossibleMoves()
            for move in possible_moves:
                print "Position: ", move.position
                cost = minimax(move)
                print "Cost: ", cost"""
            sys.stdout.flush()
            #if curr_turn =
            print "Deciding next turn..."
            sys.stdout.flush()
            next_move()
            curr_turn = OPPONENT
            numTurns+=1
            sys.stdout.flush()
        if curr_turn == OPPONENT:
            sys.stdout.flush()
            read_move()
            curr_turn = PLAYER
            numTurns+=1
            sys.stdout.flush()
main()