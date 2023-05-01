from packages import RED, WHITE, BLACK, SQUARE_SIZE, CROWN, BROWN 
import pygame

class Piece:
    PADDING = 15   # Padding size for piece circle
    OUTLINE = 2    # Outline size for piece circle

    def __init__(self, player, row, col):
        self.player = player   # The player to which the piece belongs (-1 or 1)
        self.color = RED if player == 1 else BROWN   # The color of the piece based on the player
        self.x = 0   # The x-coordinate of the piece's position on the screen
        self.y = 0   # The y-coordinate of the piece's position on the screen
        self.row = row   # The row of the piece on the board
        self.col = col   # The column of the piece on the board
        self.king = False   # Whether the piece is a king or not
        self.get_position()   # Get the position of the piece on the screen based on the board position

    def get_position(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2   # Calculate the x-coordinate of the piece on the screen
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2   # Calculate the y-coordinate of the piece on the screen

    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING   # Calculate the radius of the piece's circle
        pygame.draw.circle(win, BLACK, (self.x, self.y), radius + self.OUTLINE)   # Draw the outline of the piece's circle
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)   # Draw the piece's circle with its color
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))   # If the piece is a king, draw a crown icon on top of it

    @property
    def is_king(self):
        return self.king   # Check whether the piece is a king or not

    def promote_to_king(self):
        self.king = True   # Promote the piece to a king

    def move(self, row, col):
        self.row = row   # Update the row of the piece on the board
        self.col = col   # Update the column of the piece on the board
        self.get_position()   # Update the position of the piece on the screen

    def __repr__(self):
        # return f"Piece(color={self.color}, player={self.player}, row={self.row}, col={self.col})"
        return str(self.player)   # Return the player number of the piece as a string


