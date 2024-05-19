import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main():
    run = True
    game = Game(WIN)

    # GUI for selecting difficulty
    difficulty = None
    difficulty_selected = False
    font = pygame.font.SysFont(None, 40)

    while not difficulty_selected:
        WIN.fill((0, 0, 0))
        draw_text('Select Difficulty:', font, (255, 255, 255), WIN, 50, 50)
        draw_text('Easy', font, (255, 255, 255), WIN, 100, 150)
        draw_text('Medium', font, (255, 255, 255), WIN, 100, 200)
        draw_text('Hard', font, (255, 255, 255), WIN, 100, 250)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 100 <= x <= 250 and 150 <= y <= 180:
                    difficulty = "easy"
                    difficulty_selected = True
                elif 100 <= x <= 250 and 200 <= y <= 230:
                    difficulty = "medium"
                    difficulty_selected = True
                elif 100 <= x <= 250 and 250 <= y <= 280:
                    difficulty = "hard"
                    difficulty_selected = True

    # Assign depth based on difficulty
    if difficulty == "easy":
        choice = 4
    elif difficulty == "medium":
        choice = 8
    elif difficulty == "hard":
        choice = 50

    while run:
        if game.turn == WHITE:
            choice = int(choice)
            value, new_board = minimax(game.get_board(), choice, float('-inf'), float('inf'), True, game)
            game.ai_move(new_board)

        if game.winner() is not None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    if game.winner() == RED:
        print("RED WINS")
    else:
        print("WHITE WINS")
    pygame.quit()


main()
