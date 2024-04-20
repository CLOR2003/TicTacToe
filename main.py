import pygame
import random

# Initialize pygame
pygame.init()

# Define constants
WIDTH = 300
HEIGHT = 400
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Define functions
def draw_board():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, WHITE, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
    for j in range(1, BOARD_COLS):
        pygame.draw.line(screen, WHITE, (j * SQUARE_SIZE, 0), (j * SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)

def draw_markers(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, WHITE, (col * SQUARE_SIZE + 15, row * SQUARE_SIZE + 15), 
                                 ((col + 1) * SQUARE_SIZE - 15, (row + 1) * SQUARE_SIZE - 15), LINE_WIDTH)
                pygame.draw.line(screen, WHITE, ((col + 1) * SQUARE_SIZE - 15, row * SQUARE_SIZE + 15), 
                                 (col * SQUARE_SIZE + 15, (row + 1) * SQUARE_SIZE - 15), LINE_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 15, LINE_WIDTH)

def is_winner(board, player):
    # Check rows, columns, and diagonals
    for i in range(BOARD_ROWS):
        if all(board[i][j] == player for j in range(BOARD_COLS)):
            return True
    for j in range(BOARD_COLS):
        if all(board[i][j] == player for i in range(BOARD_ROWS)):
            return True
    if all(board[i][i] == player for i in range(BOARD_ROWS)) or all(board[i][BOARD_COLS - i - 1] == player for i in range(BOARD_ROWS)):
        return True
    return False

def is_board_full(board):
    return all(board[i][j] != ' ' for i in range(BOARD_ROWS) for j in range(BOARD_COLS))

def get_empty_positions(board):
    empty_positions = []
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if board[i][j] == ' ':
                empty_positions.append((i, j))
    return empty_positions

def minimax(board, depth, is_maximizing):
    if is_winner(board, 'O'):
        return 1
    elif is_winner(board, 'X'):
        return -1
    elif is_board_full(board):
        return 0
    
    if is_maximizing:
        max_eval = -float('inf')
        for i, j in get_empty_positions(board):
            board[i][j] = 'O'
            eval = minimax(board, depth + 1, False)
            max_eval = max(max_eval, eval)
            board[i][j] = ' '
        return max_eval
    else:
        min_eval = float('inf')
        for i, j in get_empty_positions(board):
            board[i][j] = 'X'
            eval = minimax(board, depth + 1, True)
            min_eval = min(min_eval, eval)
            board[i][j] = ' '
        return min_eval

def get_best_move(board):
    best_move = None
    best_eval = -float('inf')
    for i, j in get_empty_positions(board):
        board[i][j] = 'O'
        eval = minimax(board, 0, False)
        board[i][j] = ' '
        if eval > best_eval:
            best_eval = eval
            best_move = (i, j)
    return best_move

def display_turn(turn):
    font = pygame.font.Font(None, 36)
    if turn == 'human':
        text = font.render("Your Turn", True, WHITE)
    else:
        text = font.render("AI's Turn", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(text, text_rect)

# Add this function to randomly select who goes first
def select_first_player():
    return random.choice(['human', 'AI'])
# Add this function to reset the game state
def reset_game():
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)], select_first_player()

def display_end_screen():
    font = pygame.font.Font(None, 36)
    text_quit = font.render("Quit", True, WHITE)
    text_restart = font.render("Restart", True, WHITE)
    quit_rect = text_quit.get_rect(center=(WIDTH // 4, HEIGHT // 2))
    restart_rect = text_restart.get_rect(center=(WIDTH * 3 // 4, HEIGHT // 2))

    screen.fill(BLACK)
    screen.blit(text_quit, quit_rect)
    screen.blit(text_restart, restart_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if quit_rect.collidepoint(x, y):
                    return "quit"
                elif restart_rect.collidepoint(x, y):
                    return "restart"


# Modify the main function to include the restart option
def main():
    board, turn = reset_game()  # Initialize the game state

    while True:  # Loop until the player quits
        board, turn = reset_game()
        game_over = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and turn == 'human':
                    x, y = event.pos
                    row = y // SQUARE_SIZE
                    col = x // SQUARE_SIZE
                    if board[row][col] == ' ':
                        board[row][col] = 'X'
                        turn = 'AI'
                elif turn == 'AI':
                    row, col = get_best_move(board)
                    if board[row][col] == ' ':
                        board[row][col] = 'O'
                        turn = 'human'

            screen.fill(BLACK)
            draw_board()
            draw_markers(board)
            display_turn(turn)
            pygame.display.flip()

            if is_winner(board, 'X'):
                print("You win!")
                game_over = True
            elif is_winner(board, 'O'):
                print("AI wins!")
                game_over = True
            elif is_board_full(board):
                print("It's a draw!")
                game_over = True

        # Ask the player if they want to restart
        choice = display_end_screen()

        if choice == "quit":
            pygame.quit()
            return
            
if __name__ == "__main__":
    main()
