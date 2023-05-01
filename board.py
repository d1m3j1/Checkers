
import pygame
from copy import deepcopy
from packages import BLACK, BOARD_SIZE, RED, SQUARE_SIZE, WHITE, BLUE, DIRECTIONS 
from pieces import Piece
from game import Game
from algorithm import *

class Board():
    def __init__(self, screen, board, current_player = 1):
        # Initializes the Board object with the given screen, board, and current_player.
        # Sets the selected_piece, valid_move_squares, messages, and hint to None.
        # Draws the board and creates the pieces.
        self.screen = screen
        self.board = []
        self.selected_piece = None
        self.current_player = 1 
        self.valid_move_squares = set()
        self.messages = ""
        self.hint = None
        self.draw_board()
        self.create_pieces(board)
    
    def draw_board(self):
        # Draws the checkered board on the screen using pygame's draw.rect() function.
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, WHITE if (row + col) % 2 == 0 else BLACK, rect)

    def get_piece(self, row, col):
        # Returns the piece object at the given (row, col) position on the board.
        return self.board[row][col]

    def draw_valid_moves(self):
        # Draws green circles on the valid move squares.
        for (row, col) in self.valid_move_squares:
            pygame.draw.circle(self.screen, (0, 255, 0), (col * SQUARE_SIZE + SQUARE_SIZE // \
                2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 5)

    def draw_hint(self, hint):
        # Draws a hint on the screen using a yellow circle at the source position and a light yellow circle at the destination position.
        if hint is not None:
            src_row, src_col, dest_row, dest_col = hint
            circle_radius = SQUARE_SIZE // 5
           
            # Draw circle for source position
            rect = pygame.Rect(src_col * SQUARE_SIZE, src_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(self.screen, (255,215,0), rect, 3)
 
            # Draw circle for destination position
            dest_circle_pos = (dest_col * SQUARE_SIZE + SQUARE_SIZE // 2, dest_row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(self.screen, (255,253,208) , dest_circle_pos, circle_radius)
            
    def select(self, row, col):
        # Get the piece at the specified position on the board
        piece = self.board[row][col]
        # Check if the piece is of the same player as the current player
        if isinstance(piece, Piece) and piece.player == self.current_player:
            self.valid_move_squares.clear()
            # If there are captures available for the player
            captures = self.captures_available(self.board, self.current_player)
            if captures:
                # Generate captures for the selected piece
                piece_captures = self.generate_captures(self.board, self.current_player, row, col, piece.is_king)
                # If there are no captures for the selected piece
                if not piece_captures:
                    # Update the caption with an error message
                    self.update_caption("You must capture with another piece.")
                    self.valid_move_squares.clear()
                    self.selected_piece = None
                    self.selected_row, self.selected_col = None, None
                    return False

                # Highlight valid moves and set the selected piece
                self.selected_piece = piece
                self.selected_row, self.selected_col = row, col 
                self.highlight_valid_moves(piece_captures)
                return True
            else:
                # If there are no captures available for the player, highlight the valid moves
                self.selected_piece = piece
                self.selected_row, self.selected_col = row, col
                valid_moves = self.get_valid_moves(piece.player, row, col)
                self.highlight_valid_moves(valid_moves)
                return True
        else:
            # Clear the valid moves and selected piece if the piece selected is not of the same player
            self.valid_move_squares.clear()
            self.selected_piece = None
            self.selected_row, self.selected_col = None, None
            return False

    # Draw the selected piece if there is one
    def draw_selected_piece(self):
        if self.selected_piece is not None:
            x = self.selected_col * SQUARE_SIZE
            y = self.selected_row * SQUARE_SIZE
            pygame.draw.rect(self.screen, (0, 0, 255), (x, y, SQUARE_SIZE, SQUARE_SIZE), 3)

    # Draw the pieces on the board
    def draw_pieces(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if isinstance(piece, Piece):
                    piece.draw(self.screen)

    # Highlight valid moves for a piece by adding them to the set of valid move squares
    def highlight_valid_moves(self, moves):
        for move in moves:
            end_row, end_col = move[2], move[3]
            self.valid_move_squares.add((end_row, end_col))
        
    # Create the pieces on the board from the input board
    def create_pieces(self, board):
        for row in range(BOARD_SIZE):
            self.board.append([])
            for col in range(BOARD_SIZE):
                piece = board[row][col]
                if piece != 0:
                    piece_obj = Piece(piece, row, col)
                    self.board[row].append(piece_obj)
                else:
                    self.board[row].append(None)

    def generate_moves(self, board, player, row=None, col=None, target=None, king=False):
        moves = []  # List to store all possible moves for the player

        if row is not None and col is not None:  # If row and column arguments are provided
            piece_moves = self._generate_moves_for_piece(board, player, row, col, target, king)  # Generate moves for the specified piece
            moves.extend(piece_moves)  # Add the moves to the list of moves
            captures = self.generate_captures(board, player, row, col, king)  # Generate captures for the specified piece
            moves.extend(captures)  # Add the captures to the list of moves
        else:  # If row and column arguments are not provided
            for r in range(8):  # Loop through all rows
                for c in range(8):  # Loop through all columns
                    cell = board[r][c]  # Get the piece at the current position
                    piece = cell if isinstance(cell, Piece) else None  # If the current position has a piece object, set the piece variable, otherwise set it to None
                    if piece is not None and piece.player == player:  # If the piece belongs to the current player
                        piece_moves = self._generate_moves_for_piece(board, player, r, c, target, piece.king)  # Generate moves for the piece
                        moves.extend(piece_moves)  # Add the moves to the list of moves
                        captures = self.generate_captures(board, player, r, c, piece.king)  # Generate captures for the piece
                        moves.extend(captures)  # Add the captures to the list of moves
        return moves  # Return the list of all possible moves for the player


    def _generate_moves_for_piece(self, board, player, row, col, target=None, king=False):
        moves = []  # List to store all possible moves for the piece
        directions = DIRECTIONS  # Set the directions to move based on the player's direction
        if king:  # If the piece is a king
            directions = DIRECTIONS + DIRECTIONS  # Allow the king to move in all directions

        for dr, dc in directions:  # Loop through all the directions
            r, c = row + dr, col + dc  # Get the position after moving in the current direction
            row_diff = r - row  # Calculate the difference in rows between the current position and the new position
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] is None and ((player == 1 and row_diff > 0) or (player == -1 and row_diff < 0) or king):  # If the new position is within the board, is empty
                if target is None or (r, c) == target:
                    moves.append((row, col, r, c))
        return moves

    def generate_captures(self, board, player, row, col, king=False):
        result = []
        directions = DIRECTIONS
        if king:
            # if the piece is a king, it can move in all directions
            directions = DIRECTIONS + DIRECTIONS

        for dr, dc in directions:
            # find the coordinates of the square in the capture direction
            r, c = row + dr, col + dc
            row_diff = r - row
            if 0 <= r < 8 and 0 <= c < 8:
                # get the piece on the square, if any
                cell = board[r][c]
                piece = cell if isinstance(cell, Piece) else None
                if piece is not None and piece.player == -player:
                    # Check if the capture direction is valid (forward for regular pieces, any for kings)
                    if (player == 1 and row_diff > 0) or (player == -1 and row_diff < 0) or king:
                        # Possible capture, check if the next square in the same direction is empty
                        r, c = r + dr, c + dc
                        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] is None:
                            result.append((row, col, r, c))
                            break
        return result


    def is_valid_move(self, player, start_row, start_col, end_row, end_col, verbose=True):
        # Get the piece at the start and the target cell at the end
        piece = self.board[start_row][start_col]
        target = self.board[end_row][end_col]
        # Calculate the row and column differences between start and end positions
        row_diff = end_row - start_row
        col_diff = end_col - start_col

        # Check if the piece at the start is a valid piece for the current player
        if not isinstance(piece, Piece) or piece.player != player:
            if verbose:
                self.update_caption("Invalid move: It's not your turn.")
            return False

        # Check if the target cell is occupied by a piece of the same color
        if isinstance(target, Piece) and target.color == piece.color:
            if verbose:
                self.update_caption("Invalid move: you can't move here.")
            return False

        # Check if the target cell is already occupied by a piece
        if target is not None:
            if verbose:
                self.update_caption("Invalid move: the target position is already occupied.")
            return False

        # Check if the move is diagonal (as required by the game rules)
        if abs(row_diff) != abs(col_diff):
            if verbose:
                self.update_caption("Invalid move: you can only move diagonally.")
            return False

        # Check if the piece is not a king and is moving in the wrong direction
        if not piece.king and (player == 1 and row_diff <= 0 or player == -1 and row_diff >= 0):
            if verbose:
                self.update_caption("Invalid move: you can't move in this direction.")
            return False

        # Check if the move is a capture move (which requires jumping over another piece)
        if abs(row_diff) == 2 and abs(col_diff) == 2:
            # Calculate the middle cell (between start and end cells)
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2
            # Get the piece in the middle cell (if any)
            middle_piece = self.board[middle_row][middle_col]
            # Check if there is a piece in the middle cell and it belongs to the opponent
            if middle_piece is not None and middle_piece.player == -player:
                return True
            else:
                if verbose:
                    print("Invalid move: no piece to capture.")
                return False
        # Check if the move is a regular move (one cell diagonal)
        elif abs(row_diff) == 1 and abs(col_diff) == 1:
            return True

        return False


    def captures_available(self, board, player):
        # Iterate over all cells on the board
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                # Check if there is a piece in the current cell and it belongs to the current player
                if isinstance(board[r][c], Piece) and board[r][c].player == player:
                    # Generate all possible captures for the piece in the current cell
                    captures = self.generate_captures(board, player, r, c, board[r][c].is_king)
                    # Check if there is at least one possible capture
                    if captures:
                        return True
        return False


    def move_piece(self, start_row, start_col, end_row, end_col, player):
        # Check if move is valid
        valid_move = self.is_valid_move(player, start_row, start_col, end_row, end_col)

        if valid_move:
            # Check if captures are available
            if self.captures_available(self.board, player):
                # Generate available captures for the piece
                captures = self.generate_captures(self.board, player, start_row, start_col, self.board[start_row][start_col].is_king)
                # Check if move is a capture move
                if (start_row, start_col, end_row, end_col) not in captures:
                    self.update_caption("Invalid move. A capture is available.")
                    return False, self.board, [], player, False
            else:
                # Check if move is a capture move when no captures are available
                row_diff = end_row - start_row
                col_diff = end_col - start_col
                if abs(row_diff) == 2 and abs(col_diff) == 2:
                    print("Invalid move. You can only capture.")
                    self.update_caption("Invalid move. You can only capture.")
                    return False, self.board, [], player, False

            # Make a deep copy of the board
            updated_board = deepcopy(self.board)
            # Get the piece to be moved
            piece = updated_board[start_row][start_col]
            # Update the piece's current location on the board
            updated_board[start_row][start_col] = None
            # Move the piece to the new location on the board
            updated_board[end_row][end_col] = piece
            # Update the piece's location attribute
            piece.move(end_row, end_col)

            # Check if piece should be promoted to king
            if player == 1 and end_row == BOARD_SIZE - 1 and piece.player == 1:
                piece.promote_to_king()
                self.update_caption("Piece promoted to king!")
            if player == -1 and end_row == 0 and piece.player == -1:
                piece.promote_to_king()
                self.update_caption("Piece promoted to king!")

            # Create an empty list to store captured pieces
            captured_pieces = []

            # Calculate row and column differences
            row_diff = end_row - start_row
            col_diff = end_col - start_col

            # Set next player
            next_player = -player  # Set next_player here

            # Check if move was a capture move
            if abs(row_diff) == 2 and abs(col_diff) == 2:
                # Get location of captured piece
                middle_row = (start_row + end_row) // 2
                middle_col = (start_col + end_col) // 2
                # Remove captured piece from board
                captured_piece = updated_board[middle_row][middle_col]
                updated_board[middle_row][middle_col] = None

                # Check if piece is valid
                if isinstance(captured_piece, Piece):
                    # Add captured piece to captured_pieces list
                    captured_pieces.append((middle_row, middle_col))

                    # Check if capturing piece is promoted to king
                    if captured_piece.is_king and not piece.is_king:
                        piece.promote_to_king()
                        self.update_caption("Piece promoted to king after capturing a king!")

                # Check for additional captures
                next_capture = self.generate_captures(updated_board, player, end_row, end_col, piece.is_king)

                if next_capture:
                    # Set next player as the current player if there are additional captures
                    self.update_caption("You must continue capturing with the current piece.")
                    next_player = player  # If there are additional captures, keep the same player

                return True, updated_board, captured_pieces, next_player, next_capture
            else:
                return True, updated_board, [], -player, False

        else:
            self.update_caption("Invalid move. Please try again.")
            return False, self.board, [], player, False

    # Define a function that gets all the valid moves of the selected piece
    def get_valid_moves(self, player, row, col, target=None):
        valid_moves = []
        # Get all the normal moves that the piece can make
        moves = self.generate_moves(self.board, self.selected_piece.player, row, col, target=target, king=self.selected_piece.king)
        # Get all the captures that the piece can make
        captures = self.generate_captures(self.board, self.selected_piece.player, row, col, king=self.selected_piece.king)

        # Iterate over all the moves and captures and check if they are valid moves, then add them to the list of valid moves
        for move in moves:
            if self.is_valid_move(player, move[0], move[1], move[2], move[3]):
                valid_moves.append(move)

        for capture in captures:
            if self.is_valid_move(player, capture[0], capture[1], capture[2], capture[3]):
                valid_moves.append(capture)

        # Return the list of valid moves
        return valid_moves

    # Define a function that makes an AI move
    def ai_move(self, player, depth):
        # Add a delay to make the AI move more human-like
        pygame.time.delay(1500)
        # Get the best move using a minimax algorithm with a specified depth
        best_move = generate_best_move(self, depth)
        # Alternatively, you could also generate the best move by passing the player to the generate_best_move function:
        # best_move = generate_best_move(self, player, depth)
        if best_move is None:
            # If there is no valid move, return False with None values for the other parameters
            return False, None, None, player, False
        # Make the best move and return the values returned by the move_piece function
        start_row, start_col, end_row, end_col = best_move
        valid_move, updated_board, captured_pieces, next_player, has_more_captures = self.move_piece(start_row, start_col, end_row, end_col, player)
        return valid_move, updated_board, captured_pieces, next_player, has_more_captures

    # Define a function that checks for a winner
    def check_winner(self):
        player1_pieces = 0
        player2_pieces = 0

        # Iterate over all the squares on the board and count the number of pieces for each player
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if isinstance(piece, Piece):
                    if piece.player == 1:
                        player1_pieces += 1
                    elif piece.player == -1:
                        player2_pieces += 1

        # If one player has no pieces left, they lose and the other player wins
        if player1_pieces == 0:
            print('WHITE WINS')
            return -1  # Player 2 wins
        elif player2_pieces == 0:
            print('RED WINS')
            return 1   # Player 1 wins
        # If both players have only one piece left, it's a draw
        elif player1_pieces == 1 and player2_pieces == 1: 
            print('DRAW')
            return 'DRAW'
        else:
            # If no one has won yet, return 0
            return 0   # No winner yet

    # Define a function that updates the caption of the game window with a specified message
    def update_caption(self, message):
        pygame.display.set_caption("Checkers - " + message)



    # Check if the game is over
    def is_game_over(self):
        # Check if any player has no pieces left or has no valid moves
        for player in [1, -1]:
            if not self.has_pieces(player) or not self.has_valid_moves(player):
                return True
        return False

    # Check if a player has any pieces left on the board
    def has_pieces(self, player):
        for row in self.board:
            for piece in row:
                if piece is not None and piece.player == player:
                    return True
        return False

    # Check if a player has any valid moves
    def has_valid_moves(self, player):
        return len(self.generate_moves(self.board, player)) > 0

    # Evaluate the current state of the board and return a score
    def evaluate(self):
        score = 0
        for row in self.board:
            for piece in row:
                if piece is not None:
                    if piece.player == 1:
                        score += 1
                    elif piece.player == -1:
                        score -= 1
        return score

    # Deep copy the current instance of the Checkers class
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result

        for k, v in self.__dict__.items():
            if k == 'screen' or k == 'pieces_img':  # Skip deepcopy for Pygame Surface objects
                setattr(result, k, v)
            else:
                setattr(result, k, deepcopy(v, memo))
        return result

    # Draw the game board, pieces, valid moves, selected piece, and a hint if provided
    def draw_new_board(self, hint= None): 
        self.draw_board()
        self.draw_pieces()
        self.draw_valid_moves()
        self.draw_selected_piece()
        self.draw_hint(hint)


    # def evaluate_board(self, board):
    #     pieces_count = {1: 0, -1: 0}  # Dictionary to count the number of pieces for each player
    #     for row in range(BOARD_SIZE):
    #         for col in range(BOARD_SIZE):
    #             piece = board[row][col]  # Get the piece at the current position
    #             if isinstance(piece, Piece):  # If the current position has a piece object
    #                 pieces_count[piece.player] += 1  # Add 1 to the count for the corresponding player

    #     return pieces_count[1] - pieces_count[-1]  # Return the difference between the number of pieces for player 1 and player -1 as the score
