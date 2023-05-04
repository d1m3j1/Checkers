from packages import BOARD_SIZE
from pieces import Piece
import pygame

class Game:
    def __init__(self):
        self.red_left = self.white_left = 12  # Set the initial number of red and white pieces left on the board to 12
        self.red_king = self.white_king = 12  # Set the initial number of red and white kings left on the board to 12
        
    def create_checkerboard_array(self):
        """
        Creates a 2D array representing the checkerboard with alternating black and white squares.
        Also places initial pieces on the board in their starting positions.
        """
        array = [
            [(row + col) % 2 if row < 3 else (-1 if (row + col) % 2 == 1 else 0) if row >= 5 else 0
             for col in range(8)]
            for row in range(8)
        ]
        return array

    def count_pieces(self):
        """
        Counts the number of pieces left on the board for each player and returns the counts as a dictionary.
        """
        pieces_count = {1: 0, -1: 0}
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if isinstance(piece, Piece):
                    pieces_count[piece.player] += 1
        return pieces_count

    def update_caption(message):
        """
        Updates the caption of the Pygame window with the given message.
        """
        pygame.display.set_caption("Checkers - " + message)


