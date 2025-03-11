import pygame
import sys
import math
import random

class GameBoard:
    def __init__(self, size):
        self.size = size
        self.num_disks = [0] * size
        self.items = [[0] * size for i in range(size)]
        self.points = [0] * 2
        
    def num_free_positions_in_column(self, column):
        return self.size - self.num_disks[column]
    
    def draw_board(self, board_size):
      for c in range(board_size):
          for r in range(board_size):
              pygame.draw.rect(screen, blue, (c*squaresize, r*squaresize+squaresize, squaresize, squaresize))
              pygame.draw.circle(screen, black, (int(c*squaresize+squaresize/2), int(r*squaresize+squaresize+squaresize/2)), radius)
      
      for c in range(board_size):
          for r in range(board_size):
            if board.items[c][r] == 1:
              pygame.draw.circle(screen, red, (int(c*squaresize+squaresize/2), height-int(r*squaresize+squaresize/2)), radius)
            elif board.items[c][r] == 2:
              pygame.draw.circle(screen, yellow, (int(c*squaresize+squaresize/2), height-int(r*squaresize+squaresize/2)), radius)
      pygame.display.update()
        
    def num_new_points(self, column, row, player):
        # Checks for a newly 4-in-a-row sequence in all directions
        if player == self.items[column][row]:
            new_points = 0
            
            vertical = 0
            for i in range(row, -1, -1):
                if self.items[column][i] == player:
                    vertical += 1
                else:
                    if vertical >= 1:
                        vertical = 0
                if vertical == 4:
                    new_points += 1
                    
            horizontal = 0
            for i in range(max(0, column - 3), min(self.size, column + 4)):
                if self.items[i][row] == player:
                    horizontal += 1
                else:
                    if horizontal >= 1:
                        horizontal = 0
                if horizontal >= 4:
                    new_points += 1
            
            top_left_count = self.diagonal(column - 1, row + 1, -1, 1, column, row, player)
            bottom_right_count = self.diagonal(column + 1, row - 1, 1, -1, column, row, player)
            if top_left_count + bottom_right_count + 1 == 4:
                new_points += 1
            elif top_left_count + bottom_right_count + 1 > 4:
                new_points += 2
    
            top_right_count = self.diagonal(column + 1, row + 1, 1, 1, column, row, player)
            bottom_left_count = self.diagonal(column - 1, row - 1, -1, -1, column, row, player)
            if top_right_count + bottom_left_count + 1 == 4:
                new_points += 1
            elif top_right_count + bottom_left_count + 1 > 4:
                new_points += 2
                
            return new_points
        
        else:
            return 0
    
    def diagonal(self, start_col, start_row, d_col, d_row, column, row, player):
        count = 0
        col, row = start_col, start_row
        while max(0, column - 3) <= col < min(self.size, column + 4) and 0 <= row < self.size and self.items[col][row] == player:
            count += 1
            col += d_col
            row += d_row
        return count
    
    def add(self, column, player):
        # Adds a disk for player in a column with a empty space
        # Checks if the disk placed resulted in a point and adds a point if resulted in a point
        if column is not None:
          row = self.num_disks[column]
          self.items[column][row] = player
          self.num_disks[column] += 1
          
          points_gained = self.num_new_points(column, row, player)
          self.points[player - 1] += points_gained
        
          return row      
    
    def possible_new_points(self, col, row, player):
      self.items[col][row] = player
      result = self.num_new_points(col, row, player)
      self.items[col][row] = 0
      return result
    
    def is_board_full(self):
      for col in range(self.size):
          if board.num_free_positions_in_column(col) > 0:
              return False  
      return True

def starting_screen():
    starting = input("Welcome to Connect Four\nWould you like to play? (Y/N) ")

    while starting not in ["Y", "y", "N", "n"]:
        starting = input("Hmm? Sorry didn't quite get that. Would you like to play? (Y/N) ")
    
    if starting in ["Y", "y"]:
        board_size = int(input("Great! How big would you like your board (5-7): "))
        while not 5 <= board_size <= 7:
            board_size = int(input("Sorry, the board size should be between 5 and 7. Try again: "))
        
        gamemode = input("Press 1 for Single Player or 2 for Multi Player?: ")
        while gamemode not in ["1", "2"]:
            gamemode = input("Invalid choice! Press 1 for Single Player or 2 for Multi Player?: ")
        
        if gamemode == "1":
          difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
          while difficulty not in ["easy", "medium", "hard"]:
              difficulty = input("Invalid choice! Please choose again (easy, medium, hard): ").lower()
          return board_size, difficulty
    
    elif starting in ["N", "n"]:
        print("Okay, Goodbye!")
        board_size, difficulty = 0, None
    
    return board_size, None

def easy(board):
    valid_columns = [col for col in range(board.size) if board.num_free_positions_in_column(col) > 0]     
    if valid_columns:
        return random.choice(valid_columns)  # Choose randomly from valid columns
    else:
        print("No more valid columns! The board is full.")
        return None

def medium(board):
    for col in range(board.size):
        if board.num_free_positions_in_column(col) > 0:
            row = board.size - board.num_free_positions_in_column(col)
            result = board.possible_new_points(col, row, 1)
            if result > 0:
              return col  
            
    valid_columns = [col for col in range(board.size) if board.num_free_positions_in_column(col) > 0]     
    if valid_columns:
        return random.choice(valid_columns)  # Choose randomly from valid columns
    else:
        print("No more valid columns! The board is full.")
        return None

def hard(board):
    for col in range(board.size):
        if board.num_free_positions_in_column(col) > 0:
            row = board.size - board.num_free_positions_in_column(col)
            result = board.possible_new_points(col, row, 2)
            if result > 0:
              return col
        
    for col in range(board.size):
        if board.num_free_positions_in_column(col) > 0:
            row = board.size - board.num_free_positions_in_column(col)
            result = board.possible_new_points(col, row, 1)
            if result > 0:
              return col  
            
    valid_columns = [col for col in range(board.size) if board.num_free_positions_in_column(col) > 0]     
    if valid_columns:
        return random.choice(valid_columns)  # Choose randomly from valid columns
    else:
        print("No more valid columns! The board is full.")
        return None

board_size, difficulty = starting_screen()
if board_size == 0:
    exit()
board = GameBoard(board_size)
    
pygame.init()
squaresize = 100
width =  board_size * squaresize
height = (board_size+1) * squaresize
size = (width, height)
screen = pygame.display.set_mode(size)  
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
radius = int(squaresize/2 - 5)      
board.draw_board(board_size)
pygame.display.update()
my_font = pygame.font.SysFont("Roboto", 70)

game_over = False
turn = 0
if difficulty == None:
    while not game_over:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, squaresize))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, red, (posx, int(squaresize/2)), radius)
            else:
                pygame.draw.circle(screen, yellow, (posx, int(squaresize/2)), radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Ask for Player 1
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/squaresize))
                row = board.add(col, 1)
                if row is not None and board.num_new_points(col, row, 1) >= 1:
                      game_over = True  # Set game_over to True when Player 1 wins
                      winner = "Player 1"
              
            # Ask for Player 2
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/squaresize))
                row = board.add(col, 2)  
                if row is not None and board.num_new_points(col, row, 2) >= 1:
                      game_over = True  # Set game_over to True when Player 2 wins
                      winner = "Player 2"
                
            board.draw_board(board_size)
            turn += 1
            turn = turn % 2

if difficulty == "easy":
    while not game_over:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, squaresize))
            posx = event.pos[0]
            pygame.draw.circle(screen, red, (posx, int(squaresize/2)), radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            posx = event.pos[0]
            col = int(math.floor(posx/squaresize))
            if board.is_board_full():
                winner = "Draw"
                game_over = True
                break
                        
            if board.num_free_positions_in_column(col) > 0:
              row = board.add(col, 1)
              if row is not None and board.num_new_points(col, row, 1) >= 1:
                  game_over = True
                  winner = "Player 1"
              board.draw_board(board_size)
          
              col = easy(board)
              row = board.add(col, 2)
              if row is not None and board.num_new_points(col, row, 2) >= 1:
                  game_over = True
                  winner = "AI"
              board.draw_board(board_size)
            else:
                print(f"Column {col} is full. Please choose another column.")


if difficulty == "medium":
    while not game_over:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, squaresize))
            posx = event.pos[0]
            pygame.draw.circle(screen, red, (posx, int(squaresize/2)), radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            posx = event.pos[0]
            col = int(math.floor(posx/squaresize))
            if board.is_board_full():
                winner = "Draw"
                game_over = True
                break

            if board.num_free_positions_in_column(col) > 0:
              row = board.add(col, 1)
              if row is not None and board.num_new_points(col, row, 1) >= 1:
                  game_over = True
                  winner = "Player 1"
              board.draw_board(board_size)
          
              col = medium(board)
              row = board.add(col, 2)
              if row is not None and board.num_new_points(col, row, 2) >= 1:
                  game_over = True
                  winner = "AI"
              board.draw_board(board_size)
            else:
                print(f"Column {col} is full. Please choose another column.")

if difficulty == "hard":
    while not game_over:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, squaresize))
            posx = event.pos[0]
            pygame.draw.circle(screen, red, (posx, int(squaresize/2)), radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            posx = event.pos[0]
            col = int(math.floor(posx/squaresize))
            if board.is_board_full():
                winner = "Draw"
                game_over = True
                break

            if board.num_free_positions_in_column(col) > 0:
              row = board.add(col, 1)
              if row is not None and board.num_new_points(col, row, 1) >= 1:
                  game_over = True
                  winner = "Player 1"
              board.draw_board(board_size)
          
              col = hard(board)
              row = board.add(col, 2)
              if row is not None and board.num_new_points(col, row, 2) >= 1:
                  game_over = True
                  winner = "AI"
              board.draw_board(board_size)
            else:
                print(f"Column {col} is full. Please choose another column.")
                 
while game_over:
    screen.fill((0, 0, 0))
    if winner == "Draw":
        label = my_font.render("It's a draw!", 1, red)
    else:
        label = my_font.render(f"{winner} wins!!!", 1, red)
    screen_rect = screen.get_rect()
    label_rect = label.get_rect(center=(screen_rect.centerx, screen_rect.centery))
    screen.blit(label, label_rect)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False     

