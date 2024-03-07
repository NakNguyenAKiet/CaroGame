import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 400, 600

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Font cho text
font = pygame.font.SysFont(None, 24)

# Tạo cửa sổ
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chat App")

# Khởi tạo input box và send button
input_box = pygame.Rect(10, HEIGHT - 50, 280, 40)
send_button = pygame.Rect(300, HEIGHT - 50, 90, 40)

# Biến lưu tin nhắn và ký tự nhập
message = ""
input_text = ""

# Hàm vẽ giao diện
def draw_interface():
    win.fill(WHITE)
    pygame.draw.rect(win, GRAY, input_box, 0)
    pygame.draw.rect(win, BLACK, input_box, 2)
    pygame.draw.rect(win, BLACK, send_button, 2)

    # Vẽ tin nhắn
    text_surface = font.render(message, True, BLACK)
    win.blit(text_surface, (10, 10))

    # Vẽ input text
    input_surface = font.render(input_text, True, BLACK)
    win.blit(input_surface, (input_box.x + 5, input_box.y + 10))

    # Vẽ nút Send
    send_text = font.render("Send", True, BLACK)
    win.blit(send_text, (send_button.x + 10, send_button.y + 10))

    pygame.display.update()

# Vòng lặp chính
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if send_button.collidepoint(event.pos):
                message = input_text  # Gửi tin nhắn từ input
                input_text = ""  # Reset input text sau khi gửi
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]  # Xóa ký tự cuối cùng
            else:
                input_text += event.unicode  # Thêm ký tự vào input text

    draw_interface()
