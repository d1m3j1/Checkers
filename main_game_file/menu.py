import pygame
import os 
import sys
from packages import BLACK, SQUARE_SIZE, WHITE, RED, LIGHT_BLUE
pygame.font.init()

font = pygame.font.Font('main_game_file/8-BIT_WONDER.TTF', 60)
font1 = pygame.font.Font('main_game_file/8-BIT_WONDER.TTF', 40)
font2 = pygame.font.Font('main_game_file/8-BIT_WONDER.TTF', 30)
font3 = pygame.font.Font('main_game_file/8-BIT_WONDER.TTF', 20)
font4 = pygame.font.Font('main_game_file/8-BIT_WONDER.TTF', 10)
ARROWS = pygame.transform.scale(pygame.image.load(os.path.join('main_game_file/arrows.png')), (100,200))

# A doubly linked list is used in other to move through different tabs on the menu list

class Node: 
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None 

class DoublyLinkedList: 
    def __init__(self, value):
        # Initialize the doubly linked list with a start node
        self.start_node = Node(value)
    
    def append(self, value): 
        # Traverse to the end of the linked list
        current = self.start_node
        while current.next is not None: 
            current = current.next
        # Create a new node with the given value and add it to the end of the linked list
        new_node = Node(value)
        current.next = new_node
        new_node.prev = current

    
    def print_list(self): 
        # Traverse through the linked list and print each node's value
        current= self.start_node
        while current is not None:
            print(current.value)
            current = current.next

class Menu: 
    def __init__(self, win) -> None:
        # Initialize the Menu object with a window to draw on and a DoublyLinkedList with menu options
        self.window = win

        # Create linked list with different menu option
        self.dlist = DoublyLinkedList('START GAME')
        self.dlist.append('DIFFICULTY')
        self.dlist.append('RULES')
        self.dlist.append('QUIT')
        # Set the current node to the start node
        self.node = self.dlist.start_node
    
    def draw_menu(self): 
        # Fill the window with a light blue color
        self.window.fill(LIGHT_BLUE)
        # Draw the current menu option on the window
        self.draw_text(self.node.value, 40, SQUARE_SIZE * 4 , SQUARE_SIZE * 4 - 20)

    
    def draw_text(self, text, size, x, y ): # This function draws the text of the menu
            self.window.blit(font.render("MAIN MENU", True, BLACK), (150,150))
            self.window.blit(font3.render("UP / DOWN / ENTER / BACKSPACE", True, BLACK), (150,600))
            line2 = font3.render(text, True, BLACK) # render the text sent to the function
            text_rect = line2.get_rect()
            text_rect.center = (x,y) # Set center of the rect around the text so that it centers the text no matter its length
            self.window.blit(ARROWS, (x-50, y-100))
            self.window.blit(line2,text_rect)

    def check_events(self): 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return self.node.value    
                if event.key == pygame.K_BACKSPACE:
                    return "BACK"
                if event.key == pygame.K_DOWN:
                    if self.node.next != None:
                        self.node = self.node.next
                if event.key == pygame.K_UP:
                    if self.node.prev != None:
                        self.node = self.node.prev


    def draw_difficulty(self, current): # This function draws the difficulty menu
        self.window.fill(LIGHT_BLUE)
        self.window.blit(font1.render("GAME DIFFICULTY", True, BLACK), (150,150))
        self.window.blit(ARROWS, (SQUARE_SIZE * 4-50, SQUARE_SIZE * 4 -120))
        self.window.blit(font2.render(str(current), True, BLACK), (SQUARE_SIZE* 4 -15, SQUARE_SIZE * 4 - 40))
        if current >= 5:
            self.window.blit(font3.render("Careful The higher the level", True, BLACK), (150, 600))
            self.window.blit(font3.render("the slower the cpu will play", True, BLACK), (150, 640))

    def check_events_difficulty(self, initial_level, current_level):  # This function checks for n events that happen within the FPS rate
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    current_level += 100    
                if event.key == pygame.K_BACKSPACE: 
                    current_level = initial_level + 100
                if event.key == pygame.K_DOWN:
                    if current_level > 1:
                        current_level -= 1
                if event.key == pygame.K_UP:
                    if current_level < 9:
                        current_level += 1
        return current_level


    def draw_winner(self, winner, difficulty_level = None): # This function draws the winner screen
        self.window.fill(LIGHT_BLUE)
        self.window.blit(font.render("GAME OVER", True, BLACK), (150,150))
        if winner == RED or winner == 1:
            line2 = font3.render("You were beaten", True, BLACK)
            line3 = font3.render("By CPU level " + str(difficulty_level), True, BLACK)
        elif winner == WHITE or winner == -1:
            line2 = font3.render("You defeated", True, BLACK)
            line3 = font3.render("CPU level " + str(difficulty_level), True, BLACK) 
        elif winner == 0 or winner == 'DRAW':        
            line2 = font3.render("It Was A Draw", True, BLACK)
            line3 = font3.render("CPU level " + str(difficulty_level), True, BLACK)
        text_rect = line2.get_rect()
        text_rect.center = (SQUARE_SIZE * 4, SQUARE_SIZE * 4 - 20)
        self.window.blit(line2,text_rect)
        text_rect3 = line3.get_rect()
        text_rect3.center = (SQUARE_SIZE * 4, SQUARE_SIZE * 4 + 60)
        self.window.blit(line3,text_rect3)

    def draw_game_rules(self): 
        self.window.fill(LIGHT_BLUE)
        self.window.blit(font1.render("Rules", True, BLACK), (270, SQUARE_SIZE * 2 - 160))
        self.window.blit(font2.render("Game Rules", True, BLACK), (230, SQUARE_SIZE * 2 - 70))
        rules = [
            "1. Each player starts with 12 pieces on the board.",
            "2. Players alternate turns moving their pieces.",
            "3. Pieces move diagonally to an adjacent empty square.",
            "4. If an opponent's piece is in the next square and an empty square is behind it,",
            "   the player must capture the opponent's piece by jumping over it.",
            "5. When a piece reaches the opponent's side of the board, it becomes a king.",
            "6. Kings can move and capture pieces both forward and backward.",
            "7. Game ends when one player has no pieces left or cannot make a legal move.",
            "8. If an ordinary piece captures a king, the piece gets promoted to a king.",
            "9. Force capture is compulsory, in the case where the opponents piece is available",
            "   for capture, that's the only valid piece on the board for the current player.",
        ]

        for index, rule in enumerate(rules):
            rule_text = font4.render(rule, True, BLACK)
            self.window.blit(rule_text, (30, SQUARE_SIZE * 2 - 20 + index * 40))

        pygame.display.update()