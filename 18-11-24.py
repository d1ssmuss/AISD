import pygame

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (800, 800)
GRID_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE[0] // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Create the window
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.NOFRAME)
pygame.display.set_caption("Шахматы")

# Load images
board_image = pygame.image.load('Chess\Board.jpg')
king_image = pygame.image.load('Chess\wK.png')
black_king_image = pygame.image.load('Chess\BK.png')
black_night_image = pygame.image.load("Chess\BN.png")
white_rook_image = pygame.image.load("Chess\wR.png")

king_image = pygame.transform.smoothscale(king_image.convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE))
black_king_image = pygame.transform.smoothscale(black_king_image.convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE))
black_night_image = pygame.transform.smoothscale(black_night_image.convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE))
white_rook_image = pygame.transform.smoothscale(white_rook_image.convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE))

# Chess piece representation
white_king_pos = (7, 4)  # Starting position of the white king
black_king_pos = (0, 4)  # Starting position of the black king
black_night_pos_1 = (0, 1)  # Position of the knight
black_night_pos_2 = (0, 6)  # Position of the knight
white_rook_pos = (7, 7)  # Position of the rook

selected_square = None
selected_piece = None  # Track which piece is selected
player = None # Кто ходит первый


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


# Initialize font
font_numbers = pygame.font.Font(None, 35)
font_letters = pygame.font.Font(None, 35)


# Function to draw the chessboard
# Function to draw the chessboard
def draw_board(selected_square=None, possible_moves=[]):
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




# Main loop
running = True
dragging_piece = False
current_mouse_pos = (0, 0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # (Обработка событий мыши остается без изменений)

    # Clear the screen
    screen.fill(BLACK)

    # Get possible moves for the selected piece
    possible_moves = []
    if selected_piece == 'white':
        possible_moves = get_possible_moves(white_king_pos)
    elif selected_piece == 'black':
        possible_moves = get_possible_moves(black_king_pos)
    elif selected_piece == 'rook':
        possible_moves = get_rook_possible_moves(white_rook_pos)
    elif selected_piece == 'black_knight_1':
        possible_moves = get_knight_possible_moves(black_night_pos_1)
    elif selected_piece == 'black_knight_2':
        possible_moves = get_knight_possible_moves(black_night_pos_2)

    # Draw the board and the pieces
    draw_board(selected_square, possible_moves)

    # Отрисовка перемещаемой фигуры
    if dragging_piece:
        # Отрисовываем фигуру в текущей позиции мыши
        if selected_piece == 'white':
            screen.blit(king_image, (current_mouse_pos[0] - SQUARE_SIZE // 2, current_mouse_pos[1] - SQUARE_SIZE // 2))
        elif selected_piece == 'black':
            screen.blit(black_king_image,
                        (current_mouse_pos[0] - SQUARE_SIZE // 2, current_mouse_pos[1] - SQUARE_SIZE // 2))
        elif selected_piece == 'rook':
            screen.blit(white_rook_image,
                        (current_mouse_pos[0] - SQUARE_SIZE // 2, current_mouse_pos[1] - SQUARE_SIZE // 2))
        elif selected_piece == 'black_knight_1':
            screen.blit(black_night_image,
                        (current_mouse_pos[0] - SQUARE_SIZE // 2, current_mouse_pos[1] - SQUARE_SIZE // 2))
        elif selected_piece == 'black_knight_2':
            screen.blit(black_night_image,
                        (current_mouse_pos[0] - SQUARE_SIZE // 2, current_mouse_pos[1] - SQUARE_SIZE // 2))

    # Draw the white king at its current position
    white_king_rect = pygame.Rect(white_king_pos[1] * SQUARE_SIZE, white_king_pos[0] * SQUARE_SIZE, SQUARE_SIZE,
                                  SQUARE_SIZE)
    screen.blit(king_image, white_king_rect.topleft)  # Draw the white king image

    # Draw the black king at its current position
    black_king_rect = pygame.Rect(black_king_pos[1] * SQUARE_SIZE, black_king_pos[0] * SQUARE_SIZE, SQUARE_SIZE,
                                  SQUARE_SIZE)
    screen.blit(black_king_image, black_king_rect.topleft)  # Draw the black king image

    # Draw the first black knight at its current position
    black_night_1_rect = pygame.Rect(black_night_pos_1[1] * SQUARE_SIZE, black_night_pos_1[0] * SQUARE_SIZE,
                                     SQUARE_SIZE, SQUARE_SIZE)
    screen.blit(black_night_image, black_night_1_rect.topleft)  # Draw the first black knight image

    # Draw the second black knight at its current position
    black_night_2_rect = pygame.Rect(black_night_pos_2[1] * SQUARE_SIZE, black_night_pos_2[0] * SQUARE_SIZE,
                                     SQUARE_SIZE, SQUARE_SIZE)
    screen.blit(black_night_image, black_night_2_rect.topleft)  # Draw the second black knight image

    # Draw the white rook at its current position
    white_rook_rect = pygame.Rect(white_rook_pos[1] * SQUARE_SIZE, white_rook_pos[0] * SQUARE_SIZE, SQUARE_SIZE,
                                  SQUARE_SIZE)
    screen.blit(white_rook_image, white_rook_rect.topleft)  # Draw the white rook image

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()