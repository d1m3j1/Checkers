import pygame
import os 
import sys

#Define the size of the board and the size of each square in pixels
BOARD_SIZE= 8
SQUARE_SIZE = 100

#Define some colors using RGB values
WHITE = (255, 255, 255)
RED = (107, 75, 54)
BROWN = (248, 235, 203)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

#Define the possible directions a piece can move
DIRECTIONS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

#Create the game window with the appropriate dimensions
screen = pygame.display.set_mode((BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE))

#Load the crown image and scale it to the appropriate size
CROWN = pygame.transform.scale(pygame.image.load(os.path.join('main_game_file/crown.png')), (45,25))

def update_caption(message):
    # Update Pygame window caption with given message
    pygame.display.set_caption("Checkers - " + message)