"""
Tic Tac Toe Player
"""

import math
import copy
X = "X"
O = "O"
EMPTY = None

class InvalidAction(Exception):
    pass

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
    total = 0
    for row in board:
        for i in row:
            if i is not None:
                total += 1

    return X if total%2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = [] 
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                possible_actions.append((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    if new_board[action[0]][action[1]] is not None:
        raise InvalidAction("Action is invalid!")
    new_board[action[0]][action[1]] = player(board)
    return new_board

def is_board_full(board):
    total = 0
    for i in  range(3):
        for j in range(3):
            if board[i][j] is None:
                total += 1

    return total == 0

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    player_to_check = O if X == player(board) else X
    
    #horizontal
    horizontal =0
    vertical = 0
    diag1 = 0
    diag2 = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == player_to_check:
                horizontal += 1
            if board[j][i] == player_to_check:
                vertical += 1
        if vertical == 3 or horizontal == 3:
            return player_to_check
        vertical = 0
        horizontal = 0
        if board[i][i] == player_to_check:
            diag1 += 1
        if board[i][2-i] ==  player_to_check:
            diag2 += 1
    if diag1 == 3 or diag2 == 3:
        return player_to_check
    
    return EMPTY

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    return bool(winner(board)) or is_board_full(board)
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0

def minimax(board):
    _, best_action =  minimax_recur(board)
    return best_action

def minimax_recur(board):
    """
    Returns the optimal action for the current player on the board.
    """
    best_action = None
    if terminal(board):
        return utility(board), best_action

    #get all possible moves
    possible_actions = actions(board)
    turn_player = player(board)
    new_val=None
    
    

    if turn_player == X:  
        value = -2  
        for action in possible_actions:
            new_val, _ = minimax_recur(result(board, action))
            if new_val > value:
                value = new_val
                best_action = action
            if value == 1:
                return value, best_action

    elif turn_player == O:
        value = 2
        for action in possible_actions:
            new_val, _ = minimax_recur(result(board, action))
            if new_val < value:
                value = new_val
                best_action = action
            if value == -1:
                return value, best_action
    return value, best_action




    
