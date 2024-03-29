import pygame
import pickle
from network import Network
from game import Game
from button import Button
import sys

pygame.font.init()

ChatPanel = 400
width = 600
height = 600
win = pygame.display.set_mode((width + ChatPanel, height))
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
font = pygame.font.SysFont(None, 24)
GRAY = (200, 200, 200)

players = ["X","O"]
ChatMessage = []
input_text = ""
StartMessage = []
game = Game(0)

# Màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Khởi tạo input box và send button
input_box = pygame.Rect(WIDTH + 10, HEIGHT - 50, 280, 40)
send_button = pygame.Rect(WIDTH + 300, HEIGHT - 50, 90, 40)

# Vẽ bảng cờ
def draw_board():
    for row in range(1, BOARD_ROWS + 1):
        pygame.draw.line(win, BLACK, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS + 1):
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
        display_message(" Waiting for Player...") 
    else:
        draw_board()
        draw_figures(game.board)   
        draw_chat()
    pygame.display.update()

# Hàm vẽ giao diện chat
def draw_chat():
    pygame.draw.rect(win, GRAY, input_box, 0)
    pygame.draw.rect(win, BLACK, input_box, 2)
    pygame.draw.rect(win, BLACK, send_button, 2)

    #Player turn
    global game
    playerTurn_surface = font.render("PLAYER TURN: "+players[game.playerTurn], True, GREEN)
    win.blit(playerTurn_surface, (WIDTH + 10, 10))

    # Vẽ tin nhắn
    if len(StartMessage) > 0:
        for i, message in enumerate(StartMessage):
            text_surface = font.render(message, True, BLACK)
            win.blit(text_surface, (WIDTH + 10, 30 + i * 24))
    else:
        for i, message in enumerate(ChatMessage):
            text_surface = font.render(message, True, BLACK)
            win.blit(text_surface, (WIDTH + 10, 30 + i * 24))

    # Vẽ input text
    input_surface = font.render(input_text, True, BLACK)
    win.blit(input_surface, (input_box.x + 5, input_box.y + 10))

    # Vẽ nút Send
    send_text = font.render("Send", True, BLACK)
    win.blit(send_text, (send_button.x + 10, send_button.y + 10))

# Hiển thị tin nhắn
def display_message(message):
    pygame.draw.rect(win, BLACK, (0, HEIGHT // 2 - 50, WIDTH, 100))
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, WHITE)
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

# chơi online
def PlayOnline():
    win = pygame.display.set_mode((width + ChatPanel, height))
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = "X"
    player = n.getP()
    global ChatMessage
    global input_text
    global StartMessage
    global game
    StartMessage = ["You are player "+ player,"X play first"]

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
            ChatMessage = game.messages

            #kiểm tra khi có người chơi chat
            if len(ChatMessage) > 0:
                StartMessage = []

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
                if(mouseX < 3 and mouseY < 3):
                    if game.board[mouseY][mouseX] == '' and game.connected():
                        if(game.playerTurn == 0 and player == players[game.playerTurn]):
                            game.board[mouseY][mouseX] = player
                            game.changeTurn()
                            game = n.send(game)
                        if(game.playerTurn == 1 and player == players[game.playerTurn]):
                            game.board[mouseY][mouseX] = player
                            game.changeTurn()
                            game = n.send(game)
                if send_button.collidepoint(event.pos):
                    # Gửi tin nhắn từ input             
                    ChatMessage.append(player + " send: " + input_text)
                    # Reset input text sau khi gửi
                    input_text = ""
                    game.messages = ChatMessage
                    game = n.send(game)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Xóa ký tự cuối cùng
                elif event.key == pygame.K_RETURN:
                    # Gửi tin nhắn từ input             
                    ChatMessage.append(player + " send: " + input_text)
                    # Reset input text sau khi gửi
                    input_text = ""
                    game.messages = ChatMessage
                    game = n.send(game)
                else:
                    input_text += event.unicode


        #check player win
        if game.check_win():
            redrawWindow(win, game, player)
            display_message(players[game.winner] + " wins!") 
            game = n.send("reset")
        redrawWindow(win, game, player)

def bot_play():
    global game
    for row in range(0, 3):
        for col in range(0, 3):
            if game.board[row][col] == '':
                game.board[row][col] = 'O'
                return

# chơi với máy
def PlayWithBot():
    run = True
    win.fill(WHITE)
    draw_board()
    # Khởi tạo bảng cờ
    global game
    game.resetGame()
    player = 'X'
    draw_board()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0] // SQUARE_SIZE
                mouseY = event.pos[1] // SQUARE_SIZE

                if game.board[mouseY][mouseX] == '':
                    game.board[mouseY][mouseX] = player
                    draw_figures(game.board)
                    pygame.display.update()
                    if game.check_win():
                        display_message(players[game.winner] + " wins!")
                        run = False
                    else:
                        bot_play()
                        draw_figures(game.board)
                        pygame.display.update()
                        if game.check_win():
                            display_message(players[game.winner] + " wins!")
                            run = False

        pygame.display.update()

btns = [Button("Play Online", WIDTH//2-150, 100, (0,0,0)), Button("Play with bot", WIDTH//2-150, 400, (255,0,0))]
def menu_win():
    win = pygame.display.set_mode((width, height))
    run = True
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        for btn in btns:
            btn.draw(win)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos):
                        run = False
                        if btn.text == "Play Online":
                            PlayOnline()
                        if btn.text == "Play with bot":
                            PlayWithBot()
while True:
    menu_win()