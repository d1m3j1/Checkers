import pygame
from packages import BOARD_SIZE
from copy import deepcopy


def minimax_alpha_beta(game_state, depth, alpha, beta, is_maximizing):
    """
    Implementation of the minimax algorithm with alpha-beta pruning for game AI.
    :param game_state: Current state of the game.
    :param depth: The depth of the search tree.
    :param alpha: The maximum lower bound of possible values.
    :param beta: The minimum upper bound of possible values.
    :param is_maximizing: Boolean indicating whether to maximize or minimize the evaluation score.
    :return: The evaluation score of the game state.
    """
    if depth == 0 or game_state.is_game_over():
        return game_state.evaluate()

    if is_maximizing:
        max_eval = float('-inf')
        moves = game_state.generate_moves(game_state.board, 1)
        for move in moves:
            valid_move, new_board, captured_pieces, next_player, has_more_captures = game_state.move_piece(move[0], move[1], move[2], move[3], 1)
            if valid_move:
                new_board_object = deepcopy(game_state)
                new_board_object.board = new_board
                eval = minimax_alpha_beta(new_board_object, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        moves = game_state.generate_moves(game_state.board, -1)
        for move in moves:
            valid_move, new_board, captured_pieces, next_player, has_more_captures = game_state.move_piece(move[0], move[1], move[2], move[3], -1)
            if valid_move:
                new_board_object = deepcopy(game_state)
                new_board_object.board = new_board
                eval = minimax_alpha_beta(new_board_object, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def generate_best_move(board, depth: int, player=None):
    """
    Generates the best move for the given player at the given depth using the minimax algorithm.
    :param board: Current state of the game board.
    :param depth: The depth of the search tree.
    :param player: The player for whom the best move is to be generated.
    :return: The best move as a tuple of starting and ending positions of the piece being moved.
    """
    if player is None:
        player = board.current_player
    best_score = float('-inf') if player == 1 else float('inf')
    best_move = None

    all_valid_moves = board.generate_moves(board.board, player)
    for move in all_valid_moves:
        valid_move, new_board, captured_pieces, next_player, has_more_captures = board.move_piece(move[0], move[1], move[2], move[3], player)
        if valid_move:
            new_board_object = deepcopy(board)
            new_board_object.board = new_board
            score = minimax_alpha_beta(new_board_object, depth - 1, float('-inf'), float('inf'), player != 1)
            
            if player == 1 and score > best_score:
                best_score = score
                best_move = move
            elif player == -1 and score < best_score:
                best_score = score
                best_move = move
                
    return best_move

