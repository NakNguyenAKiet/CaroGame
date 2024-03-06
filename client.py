import pygame
import pickle
from network import Network
from game import Game
import sys

pygame.font.init()

width = 600
height = 600
win = pygame.display.set_mode((width, height))
pygame.init()
pygame.display.set_caption("Caro Game")
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


# Vẽ bảng cờ
def draw_board():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(win, BLACK, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(win, BLACK, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(win, RED, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(win, RED, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(win, BLUE, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, LINE_WIDTH)

def redrawWindow(win, game, p):
    win.fill((128,128,128))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        draw_board()
        draw_figures(game.board)   

    pygame.display.update()

# Hiển thị tin nhắn
def display_message(message):
    pygame.draw.rect(win, BLACK, (0, HEIGHT // 2 - 50, WIDTH, 100))
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, WHITE)
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

btns = [Button("Rock", 50, 500, (0,0,0)), Button("Scissors", 250, 500, (255,0,0)), Button("Paper", 450, 500, (0,255,0))]

players = ["X","O"]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = "X"
    player = n.getP()
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0] // SQUARE_SIZE
                mouseY = event.pos[1] // SQUARE_SIZE

                if game.board[mouseY][mouseX] == '' and game.connected():
                    if(game.playerTurn == 0 and player == players[game.playerTurn]):
                        game.board[mouseY][mouseX] = player
                        game.changeTurn()
                        game = n.send(game)
                    if(game.playerTurn == 1 and player == players[game.playerTurn]):
                        game.board[mouseY][mouseX] = player
                        game.changeTurn()
                        game = n.send(game)

        #check player win
        if game.check_win():
            redrawWindow(win, game, player)
            display_message(players[game.winner] + " wins!") 
            game = n.send("reset")

        redrawWindow(win, game, player)

# def menu_win():
#     run = True
#     clock = pygame.time.Clock()

#     while run:
#         clock.tick(60)
#         win.fill((128, 128, 128))
#         font = pygame.font.SysFont("comicsans", 60)
#         text = font.render("Click to Play!", 1, (255,0,0))
#         win.blit(text, (100,200))
#         pygame.display.update()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 run = False
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 run = False

main()

# while True:
#     menu_win()