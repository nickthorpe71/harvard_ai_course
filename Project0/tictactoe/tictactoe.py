"""
Tic Tac Toe Player
"""

import math
import copy

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


def loop_board_by_ele(board, func):
    for i in range(len(board)):
        for j in range(len(board[i])):
            func(board[i][j])


def loop_board_by_indx(board, func):
    for i in range(len(board)):
        for j in range(len(board[i])):
            func(i, j)


def map_board_to_array(board, func):
    new_arr = []
    loop_board_by_ele(board, lambda e: new_arr.append(func(e)))
    return new_arr


def is_player(element):
    return False if element == EMPTY else True


def is_specific_player(element, player):
    return element if element == player else None


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xs = map_board_to_array(board, lambda e: is_specific_player(e, X))
    os = map_board_to_array(board, lambda e: is_specific_player(e, O))
    return O if xs.count(X) >= os.count(O) else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()
    loop_board_by_indx(board, lambda i, j: result.add(
        (i, j)) if not is_player(board[i][j]) else None)
    return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError('Not a valid action')

    board_copy = copy.deepcopy(board)
    symbol = player(board)

    board_copy[action[0]][action[1]] = symbol
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win_combos = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    x_combos = 0
    o_combos = 0

    for combo in win_combos:
        x = 0
        o = 0
        for action in combo:
            if board[action[0]][action[1]] == X:
                x += 1
            if board[action[0]][action[1]] == O:
                o += 1
        if x == 3:
            x_combos += 1
        if o == 3:
            o_combos += 1

    if x_combos > 0:
        return X
    elif o_combos > 0:
        return O
    else:
        return None


def terminal(board) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    acc = True
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                acc = False
    return acc


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    res_dict = {X: 1, O: -1, EMPTY: 0}
    return res_dict[winner(board)]


def max(board):
    """
    Returns the optimal action for the max player
    """
    optimal_move = ()
    if terminal(board):
        return utility(board), optimal_move
    else:
        v = - 2
        for action in actions(board):
            min_val = min(result(board, action))[0]
            if min_val > v:
                v = min_val
                optimal_move = action
        return v, optimal_move


def min(board):
    """
    Returns the optimal action for the min player
    """
    optimal_move = ()
    if terminal(board):
        return utility(board), optimal_move
    else:
        v = 2
        for action in actions(board):
            max_val = max(result(board, action))[0]
            if max_val < v:
                v = max_val
                optimal_move = action
        return v, optimal_move


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)

    if terminal(board):
        return None

    elif current_player == X:
        return max(board)[1]

    else:
        return min(board)[1]
