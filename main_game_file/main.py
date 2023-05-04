import pygame
from packages import SQUARE_SIZE, screen
from game import Game
from board import Board
from menu import Menu
from algorithm import *

FPS = 60
HINT_DISPLAY_EVENT = pygame.USEREVENT + 1
global difficulty_level 
difficulty_level = 3

# Function to get the row and column of the square that was clicked on by the mouse
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# Function to display the main menu and wait for user input
def welcome(): 
    run = True
    clock = pygame.time.Clock()
    m = Menu(screen)
    
    pygame.display.set_caption('Main Menu')
    while run: 
        clock.tick(FPS)
        m.draw_menu() # Draw the menu
        value = m.check_events() # Check for user input
        if value == 'START GAME': # If user clicked "start game", start the game
            main()
        elif value == 'DIFFICULTY': # If user clicked "difficulty", go to the difficulty screen
            welcome_difficulty()
            pass
        elif value == 'RULES': # If user clicked "rules", show the rules screen
            game_rules()
        elif value == 'QUIT': # If user clicked "quit", quit the game
            run = False
        
        pygame.display.update()

# Function to display the difficulty screen and wait for user input
def welcome_difficulty(): # Screen in the main menu to set difficulty level of the AI
    run = True
    clock = pygame.time.Clock()
    m = Menu(screen)
    pygame.display.set_caption('Difficulty')
    global difficulty_level
    initdif = difficulty_level # Set initial difficulty when the screen was called to use it when backspace is pressed
    currentdif = initdif
    while run:
        clock.tick(FPS)
        m.draw_difficulty(currentdif) # Draw the difficulty screen
        currentdif = m.check_events_difficulty(initdif, currentdif) # Check for user input and update the selected difficulty level
        if currentdif > 100: # This is used to detect wether backspace or return keys were pressed
            currentdif -= 100 # This reverts the value to its correct one
            run = False
        pygame.display.update()
    difficulty_level = currentdif # Set global variable with the selected difficulty

# Function to display the rules screen and wait for user input
def game_rules(): # Draw credits screen and wait for backspace to be pressed to go back.
    run = True
    clock = pygame.time.Clock()
    m = Menu(screen)
    pygame.display.set_caption('Game Rules')
    while run:
        m.draw_game_rules() # Draw the rules screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE: # If user presses backspace, go back to the main menu
                run = False
                welcome()

        pygame.display.update()
 
# define main function
def main():
    # set variables
    run = True
    clock = pygame.time.Clock()
    game = Game()
    # create a board object
    board = Board(screen, game.create_checkerboard_array())
    start_row, start_col = None, None
    last_capturing_piece = None
    hints_remaining = 3
    depth = 1

    # game loop
    while run:
        # set game clock
        clock.tick(FPS)

        # check if it's AI's turn to move
        if board.current_player == 1:
            # get AI's move
            valid_move, updated_board, captured_pieces, next_player, has_more_captures = board.ai_move(board.current_player, difficulty_level)
            if valid_move:
                # update board with AI's move
                board.current_player = next_player
                board.board = updated_board
                # check for winner
                winner = board.check_winner()
                if winner != 0:
                    # draw winner
                    draw_winner(winner)
                    run = False

        # handle events
        for event in pygame.event.get():
            # quit game on close button click
            if event.type == pygame.QUIT:
                run = False
            
            # handle hint event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h and hints_remaining > 0:
                    # Give a hint to player -1
                    hint = generate_best_move(board, 4, -1)  
                    hints_remaining -= 1            
                    board.hint = hint
                    # set hint display timer
                    pygame.time.set_timer(HINT_DISPLAY_EVENT, 3000)
        
            # reset hint attribute when timer is up
            if event.type == HINT_DISPLAY_EVENT:
                board.hint = None  
                # stop the timer
                pygame.time.set_timer(HINT_DISPLAY_EVENT, 0)  

            # handle mouse button click
            if event.type == pygame.MOUSEBUTTONDOWN and board.current_player == -1:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                if last_capturing_piece is None or (row, col) == last_capturing_piece or (start_row, start_col) == last_capturing_piece:
                    if last_capturing_piece is not None and (start_row, start_col) != last_capturing_piece:
                        # continue capturing with the last capturing piece
                        start_row, start_col = last_capturing_piece
                    elif board.select(row, col):
                        # select a piece to move
                        start_row, start_col = row, col
                    elif start_row is not None and start_col is not None:
                        # move selected piece
                        valid_move, updated_board, captured_pieces, next_player, has_more_captures = board.move_piece(start_row, start_col, row, col, board.current_player)
                        if valid_move:
                            # update board with moved piece
                            board.current_player = next_player
                            board.board = updated_board
                            # check for winner
                            winner = board.check_winner()
                            if winner != 0:
                                # draw winner
                                draw_winner(winner)
                                run = False
                            if has_more_captures and captured_pieces:
                                # if there are more captures, update last capturing piece
                                last_capturing_piece = (row, col) 
                            else:
                                last_capturing_piece = None
                        else:
                            print("Invalid move. Please try again.")
                    else:
                        board.update_caption("Please select a piece to move.")
                else:
                    board.update_caption("You must continue capturing with the current piece.")
        winner = board.check_winner()
        board.draw_new_board(board.hint)
        pygame.display.update()

    pygame.quit()

def draw_winner(winner): 
    run = True
    clock = pygame.time.Clock()
    m = Menu(screen)  # Create a Menu object to display winner message
    pygame.display.set_caption('GAME OVER')  # Set the caption of the window to 'GAME OVER'
    
    while run:
        m.draw_winner(winner, difficulty_level)  # Draw the winner message on the screen
        for event in pygame.event.get():  # Loop through all pygame events
            if event.type == pygame.QUIT:  # If user closes the window
                run = False  # Exit the loop and end the program
        
        if winner is not None:  # If there is a winner
            pygame.display.update()  # Update the screen
            pygame.time.delay(5000)  # Wait for 5000 milliseconds or (5 seconds)
            run = False  # Exit the loop and end the program
        pygame.display.update()  # Update the screen

    pygame.quit()



welcome()