"""
Tic Tac Toe Player
"""

import math
import copy
import random


X = "X"
O = "O"
EMPTY = None


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
    empty_fields = 0
    for row in board:
        empty_fields += row.count(None)
    return O if empty_fields % 2 == 0 else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    poss_actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == None:
                poss_actions.add((i, j))
    return poss_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    if action[0] > 2 or action[1] > 2 or (new_board[action[0]][action[1]] != None):
        raise Exception
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for l in range(len(board)):
        if board[l][0] == board[l][1] == board[l][2] != None:
            return board[l][0]
        if board[0][l] == board[1][l] == board[2][l] != None:
            return board[0][l]
    if (board[0][0] == board[1][1] == board[2][2] != None) or (board[0][2] == board[1][1] == board[2][0] != None):
        return board[1][1]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    empty_fields = 0
    for row in board:
        empty_fields += row.count(None)

    return bool(winner(board) or empty_fields == 0)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    possible_actions = actions(board)
    current_player = player(board)
    action_value_pairs = set()

    if board == initial_state():
        return random.choice(tuple(possible_actions))

    for action in possible_actions:
        resulting_board = result(board, action)
        if (terminal(resulting_board)) and (winner(resulting_board) == current_player):
            return action
        action_value_pairs.add((action, calc_value(resulting_board)))

    if current_player == X:
        best_result = max(pair[1] for pair in action_value_pairs)
    else:
        best_result = min(pair[1] for pair in action_value_pairs)

    return [pair[0] for pair in action_value_pairs if pair[1] == best_result][0]


def calc_value(board):
    possible_actions = actions(board)
    current_player = player(board)
    action_values = set()

    if terminal(board):
        return utility(board)

    for action in possible_actions:
        resulting_board = result(board, action)
        if terminal(resulting_board):
            action_values.add(utility(resulting_board))
        else:
            action_values.add(calc_value(resulting_board))

    if current_player == X:
        return max(action_values)
    else:
        return min(action_values)
