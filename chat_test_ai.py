import pygame
import sys

# Initialize Pygame
pygame.init()

# Заметки
"""
1. Добавить рокировку
2. Ходить по клеточкам(зелёные кружочки)
2.1 Передвигаться с помощью кнопки мыши
3. Проверка на шах и мат + ничья
4. Фигуры пропадают на доске и в массиве board
5. Добавить справа мини-панельку(нотация ходов)
6. Ситуация: Если Ладья || Король ходил(-а), отключить рокировку
7. Подсвечивать если шах, мат, пат
8. Отключить возможность ходить. После мата, пата
9. Перезапуск(хотите начать новую игру?)
10. Смена ходов
11. Короли не могут находиться рядом, посмотреть условие на связку вилку итд
12. Считается ли ход, если нажму на одну и ту же клетку????????


Рокировка : 
1) Если король и ладья стоят на своих начальных местах и ещё не ходили
2) Король не должен находиться под шахом
3) Король при рокировке не имеет права прыгать через битое поле
4) Ладья при длинной рокировке имеет право перелететь через битое поле b1
5) Если фигура перекрывает диагональ при короткой рокировке, ход запрещён
6) Если между королём и ладьёй на доске нет других шахматных фигур, рокировка допускается



В массивах возможных ходов, не должны быть ходы, где есть фигуры
Справа должно быть меню кто ходит, ход AI, оценка хода, рестарт выйти из игры
Подсвечивать две последние клетки-ходы игрока(или ИИ)



Где находится функция, отвечающая за передвижение фигуры

Проверка на двойной шах
"""

# Переменные
WINDOW_SIZE = (800, 800)
GRID_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE[0] // GRID_SIZE  # 100

# Зачем тут цвета?
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание окна
# screen = pygame.display.set_mode(WINDOW_SIZE, pygame.NOFRAME)
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Шахматы v1.0 by d1ssmuss")

# Текстуры фигур
board_image = pygame.image.load('Chess/Board.jpg') # доска
king_image = pygame.image.load('Chess/wK.png') # белый король
black_king_image = pygame.image.load('Chess/BK.png') # чёрный король 
black_night_image = pygame.image.load("Chess/BN.png") # черный конь
white_rook_image = pygame.image.load("Chess/wR.png") # белая ладья

# Преобразовываем изображения, учитывая масштаб
king_image = pygame.transform.smoothscale(king_image.convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE))
black_king_image = pygame.transform.smoothscale(black_king_image.convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE))
black_night_image = pygame.transform.smoothscale(black_night_image.convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE))
white_rook_image = pygame.transform.smoothscale(white_rook_image.convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE))

# Расположение шахматных фигур X, Y
# Обратить внимание что начало координат начинается с левого верхнего угла

white_king_pos = (7, 4)
black_king_pos = (0, 4)
black_night_pos_1 = (0, 1)
black_night_pos_2 = (0, 6)
white_rook_pos = (7, 7)

selected_piece = None  # Отслеживание какая фигура выбрана
selected_square = None  # ????
player = None # Кто ходит первый

# Initialize font
font_numbers = pygame.font.Font(None, 35)
font_letters = pygame.font.Font(None, 35)

board = [
    ["", "♞", "", "", "♚", "", "♞", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "♔", "", "", "♖"]
]

# Function to draw the chessboard
def draw_board():
    # Draw the board image as background
    screen.blit(board_image, (0, 0))
    # Draw letters and numbers on the board
    for i in range(GRID_SIZE):
        # Draw numbers on the left side
        color_for_black_square = (157, 107, 70, 255)  # Blue color for letters
        color_for_white_square = (238, 218, 183, 255)  # Blue color for letters
        if i % 2 == 0:
            number_text = font_numbers.render(str(GRID_SIZE - i), True, color_for_white_square)
            letter_text = font_letters.render(chr(97 + i), True, color_for_white_square)  # 97 is the ASCII value for 'a'
        else:
            number_text = font_numbers.render(str(GRID_SIZE - i), True, color_for_black_square)
            letter_text = font_letters.render(chr(97 + i), True, color_for_black_square)  # 97 is the ASCII value for 'a'
        screen.blit(number_text, (785, (i * SQUARE_SIZE + SQUARE_SIZE // 2 - number_text.get_height() // 2) - 35))
        screen.blit(letter_text,
                    ((i * SQUARE_SIZE + SQUARE_SIZE // 2 - letter_text.get_width() // 2) - 40,
                     WINDOW_SIZE[0] - 27))  # Adjust the position as needed

dict = {
    0 : "a",
    1 : "b",
    2 : "c",
    3 : "d",
    4 : "e",
    5 : "f",
    6 : "g",
    7 : "h"
}
def draw_moves_king(x, y):  # отрисовка ходов короля
    # (для теста) нужно брать, если король у края доски
    possible_moves_king = []

    # передаю внутри функции координаты короля
    for j in range(y-1, y+2): # y
        for i in range(x-1, x+2): # x
            if (0 <= i <= 7 and 0 <= j <= 7) and (i != x or y != j):
                possible_moves_king.append([dict[j], 8 - i])
                # pygame.draw.circle(screen, (230, 50, 230), [white_king_pos[1] * SQUARE_SIZE + SQUARE_SIZE // 2, white_king_pos[0] * SQUARE_SIZE + SQUARE_SIZE // 2], 20)
                pygame.draw.circle(screen, (50, 212, 45), [j * SQUARE_SIZE + SQUARE_SIZE // 2, (i) * SQUARE_SIZE + SQUARE_SIZE // 2], 15)
    return f"{possible_moves_king}, Расположение Короля {dict[y]}{8-x}, len:{len(possible_moves_king)}"
    # вроде работает


def draw_moves_rook(x, y):  # отрисовка ходов ладьи
    possible_moves_rook = []
    # передаю внутри функции координаты короля
    for j in range(0, 8): # y
        for i in range(0, 8): # x
            if (0 <= i <= 7 and 0 <= j <= 7) and (i != x or y != j) and (x == i and j != y or x != i and j == y):
                possible_moves_rook.append([dict[j], 8 - i])    
                pygame.draw.circle(screen, (50, 212, 45), [j * SQUARE_SIZE + SQUARE_SIZE // 2, (i) * SQUARE_SIZE + SQUARE_SIZE // 2], 15)
    return f"{possible_moves_rook}, Расположение Ладьи {dict[y]}{8-x}, len:{len(possible_moves_rook)}"

current_mouse_pos = (0, 0)
# Главный цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # для закрытия окна
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:  # 
            mouse_x, mouse_y = event.pos
            column = mouse_x // SQUARE_SIZE
            row = mouse_y // SQUARE_SIZE
            
            # Если фигура выбрана
            if selected_piece:
                # Move the selected piece to the clicked square
                if selected_piece == 'white_king' and (abs(row - white_king_pos[0]) <= 1 and abs(column - white_king_pos[1]) <= 1):
                    white_king_pos = (row, column)
                    print("фигуру поставили")
                    # Вызываю функцию отображения квадратов(клеток), куда может ходить король
                    print(draw_moves_king(row,column), row, column)
            
                elif selected_piece == 'black_king' and (abs(row - black_king_pos[0]) <= 1 and abs(column - black_king_pos[1]) <= 1):
                    black_king_pos = (row, column)
                    print("фигуру поставили")

                    """# Вызываю функцию отображения квадратов(клеток), куда может ходить король
                    print(draw_moves_king(row,column))""" # ??


                elif selected_piece == 'white_rook' and (row == white_rook_pos[0] or column == white_rook_pos[1]):
                    white_rook_pos = (row, column)

                    # Вызываю функцию отображения квадратов(клеток), куда может ходить ладья
                    print(draw_moves_rook(row,column))
                    print("фигуру поставили")

                
                # Deselect the piece
                selected_piece = None
            else:
                # Select a piece if clicked
                if (row, column) == white_king_pos:
                    selected_piece = 'white_king'
                    print("Взяли Белого Короля")
                elif (row, column) == black_king_pos:
                    selected_piece = 'black_king'
                    print("Взят Чёрный Король")
                elif (row, column) == white_rook_pos:
                    selected_piece = 'white_rook'
                    print("Взята Белая Ладья")


    # Clear the screen
    screen.fill(BLACK)  # думаю можно будет убрать в будущем
    
    # Draw the board and the pieces
    draw_board()



    # draw_moves_king(4,4)  # Здесь функция работает
    # Если я хочу что-нибудь добавить на экран, то нужно добавлять внизу, т.к перед draw_board(), отрисовываться не будет, ибо идёт отрисовка

    # Draw the white king at its current position
    white_king_rect = pygame.Rect(white_king_pos[1] * SQUARE_SIZE, white_king_pos[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    screen.blit(king_image, white_king_rect.topleft)

    # Draw the black king at its current position
    black_king_rect = pygame.Rect(black_king_pos[1] * SQUARE_SIZE, black_king_pos[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    screen.blit(black_king_image, black_king_rect.topleft)

    # Draw the first black knight at its current position
    black_night_1_rect = pygame.Rect(black_night_pos_1[1] * SQUARE_SIZE, black_night_pos_1[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    screen.blit(black_night_image, black_night_1_rect.topleft)

    # Draw the second black knight at its current position
    black_night_2_rect = pygame.Rect(black_night_pos_2[1] * SQUARE_SIZE, black_night_pos_2[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        # Draw the second black knight at its current position
    black_night_2_rect = pygame.Rect(black_night_pos_2[1] * SQUARE_SIZE, black_night_pos_2[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    screen.blit(black_night_image, black_night_2_rect.topleft)

    # Draw the white rook at its current position
    white_rook_rect = pygame.Rect(white_rook_pos[1] * SQUARE_SIZE, white_rook_pos[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    screen.blit(white_rook_image, white_rook_rect.topleft)

    # Optional: Highlight the selected piecex
    # Если выбрана фигура
    if selected_piece:
        if selected_piece == 'white_king':
            pygame.draw.rect(screen, (0, 255, 0), white_king_rect, 5)  # Green border for selected piece
            draw_moves_king(white_king_pos[0],white_king_pos[1])

        elif selected_piece == 'black_king':
            pygame.draw.rect(screen, (0, 255, 0), black_king_rect, 5)  # Green border for selected piece
            draw_moves_king(black_king_pos[0],black_king_pos[1])
        elif selected_piece == 'white_rook':
            pygame.draw.rect(screen, (0, 255, 0), white_rook_rect, 5)  # Green border for selected piece
            draw_moves_rook(white_rook_pos[0],white_rook_pos[1])

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()