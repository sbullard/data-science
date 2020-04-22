"""
Tic Tac Toe Player
"""

import math
import copy
import numpy as np
from collections import Counter

X = "X"
O = "O"
EMPTY = None

""
def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    counts = Counter(board[0] + board[1] + board[2])
    
    if all(val is None for val in board):
        return(X)
    elif counts['X'] <= counts ['O']:
        return(X)
    else:
        return(O)
    
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    a = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                a.add((i,j))
    return(a)
                
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    
    if board[action[0]][action[1]] != None:
        raise Exception('Not A Valid Move')
        
    new_board[action[0]][action[1]] = player(board)
    return (new_board)
    
    
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    vert_board = np.array(board).T.tolist()
    
    diag_board = [[board[0][0], board[1][1], board[2][2]], 
                  [board[0][2], board[1][1], board[2][0]]]

    counts = Counter(board[0] + board[1] + board[2])
    
    # Game has to be over if all squares filled
    if counts[None] == 0:
        return True

    # Horizontal game over check
    for lst in board:
        if(len(set(lst))==1) and lst[0] != None:
            return True
        
    # Vertical game over check   
    for lst in vert_board:
        if(len(set(lst))==1) and lst[0] != None:
            return True
        
    # Diagonal game over check 
    for lst in diag_board:
        if(len(set(lst))==1) and lst[0] != None:
            return True   
    return False


def winner(board):
    vert_board = np.array(board).T.tolist()
    
    diag_board = [[board[0][0], board[1][1], board[2][2]], 
                  [board[0][2], board[1][1], board[2][0]]]
    
    all_boards = board + vert_board + diag_board
    
    # Check all 3-combination rows, 
    # if one has all three as X or O, return the winner
    for lst in all_boards:
        if len(set(lst)) == 1 and lst[0] != None:
            return lst[0]   
    return None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    #print(board)
    if winner(board) == 'X':
        return 1
    elif winner(board) == 'O':
        return -1
    else:
        return 0

      
# MAX Player Logic:
def maxValue(board):
    plyr = 'playerX just moved, this is the board after'
    if terminal(board):
        return utility(board)
    else:
        v = -1
        for action in actions(board):
            # Gets the largest min value of all possible
            # future MIN player moves.
            v = max(v, minValue(result(board, action)))
        return v

# MIN Player Logic:
def minValue(board):
    plyr = 'playerO just moved, this is the board after'
    if terminal(board):
        return utility(board)
    else:
        v = 1
        for action in actions(board):             
            # Gets the smallest max value of all possible future
            # MAX player moves.)
            v = min(v, maxValue(result(board, action)))  
        return v    
        

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    ai = player(board)
    best_move = ()
    
    outcomes = []
    
    # Alpha-Beta Pruning Logic to improve AI speed
    
    # 1. If board empty, take middle square
    if len(actions(board)) == 9:
        return (1,1)
    
    # 2. If length of board is 8 and middle square empty, take it
    if len(actions(board)) == 8 and board[1][1] == None:
        return(1,1)
    
    # 3. If length of board is 8 and middle square taken, get corner
    if len(actions(board)) == 8 and board[1][1] != None:
        return(0,0)
    
    # Get all remaining possible outcomes for ai move using minimax
    for move in actions(board):
        if ai == 'X':
            val = minValue(result(board, move))  
        else:
            val = maxValue(result(board, move)) 
        outcomes.append((val, move))
  
    # Return best possible move for ai
    if ai == 'X': 
        return max(outcomes)[1]
    else:
        return min(outcomes)[1]
      

