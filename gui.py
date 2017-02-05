#! /usr/bin/env python

from constants import BLACK, WHITE, DISPLAY_HEIGHT, DISPLAY_WIDTH, GLOBAL_OFFSET
from constants import SCORE_POS_X, SCORE_POS_Y, TILE_SIZE, FONT_SIZE, ICON_SIZE
import pygame
from reversi import Reversi

PIECES  = pygame.image.load('marbles.png')
TILES   = pygame.image.load('marble.png')
MOVES   = pygame.image.load('icons.png')
DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))


def run_game():
    pygame.init()
    pygame.display.set_caption('Reversi')

    clock     = pygame.time.Clock()
    game_over = False
    game      = Reversi()

    while not game_over:
        game.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                get_input(game)

        draw(game)
        clock.tick(60)
        game_over = game_over or game.game_over

    end_game(game)
    quit()


def draw(game):
    draw_board(game.board.size, game.board.size)
    draw_pieces(game)
    draw_score(game)
    if game.board.turn is BLACK:
        draw_moves(game)
    draw_button(game)
    draw_working(game)
    pygame.display.update()


def end_game(game):
    score = game.score
    winner = 'Black' if (score[BLACK] > score[WHITE]) else 'White'
    if score[BLACK] == score[WHITE]:
        winner = 'Nobody - Draw'

    print('Game over!')
    print('Score (black/white): {}/{}'.format(score[BLACK], score[WHITE]))
    print('Winner is: {}'.format(winner))
    pygame.time.wait(1500)
    pygame.quit()


def draw_button(game):
    if game.hints:
        DISPLAY.blit(MOVES, (SCORE_POS_X + TILE_SIZE // 4 + GLOBAL_OFFSET,
                             SCORE_POS_Y - 1 * TILE_SIZE + GLOBAL_OFFSET),
                            (0, 4 * ICON_SIZE, ICON_SIZE, ICON_SIZE))
    else:
        DISPLAY.blit(MOVES, (SCORE_POS_X + TILE_SIZE // 4 + GLOBAL_OFFSET,
                             SCORE_POS_Y - 1 * TILE_SIZE + GLOBAL_OFFSET),
                            (ICON_SIZE, 4 * ICON_SIZE, ICON_SIZE, ICON_SIZE))


def draw_working(game):
    if game.board.turn is BLACK:
        DISPLAY.blit(MOVES, (SCORE_POS_X - 3 * ICON_SIZE // 2 + GLOBAL_OFFSET,
                             SCORE_POS_Y  + ICON_SIZE // 2 + GLOBAL_OFFSET),
                            (3 * ICON_SIZE, 4 * ICON_SIZE, ICON_SIZE, ICON_SIZE)
                     )
    else:
        DISPLAY.blit(MOVES, (SCORE_POS_X - 3 * ICON_SIZE // 2 + GLOBAL_OFFSET,
                             SCORE_POS_Y  + 5 * ICON_SIZE // 2 + GLOBAL_OFFSET),
                            (3 * ICON_SIZE, 4 * ICON_SIZE, ICON_SIZE, ICON_SIZE)
                     )


def draw_score(game):
    score = game.score
    draw_text(str(score[BLACK]),
              (SCORE_POS_X + TILE_SIZE + FONT_SIZE // 2,
               SCORE_POS_Y + FONT_SIZE // 2))
    draw_text(str(score[WHITE]),
              (SCORE_POS_X + TILE_SIZE + FONT_SIZE // 2,
               SCORE_POS_Y + FONT_SIZE // 2 + TILE_SIZE))
    draw_piece(SCORE_POS_X, SCORE_POS_Y, 'black')
    draw_piece(SCORE_POS_X, SCORE_POS_Y + TILE_SIZE, 'white')


def draw_text(text, pos, color=(0, 0, 0)):
    pos = (pos[0] + GLOBAL_OFFSET, pos[1] + GLOBAL_OFFSET)
    font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    rect.topleft = (pos)
    DISPLAY.blit(surface, rect)


def get_input(game):
    pos  = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    row = (int(pos[1]) - GLOBAL_OFFSET) // TILE_SIZE + 1
    col = (int(pos[0]) - GLOBAL_OFFSET) // TILE_SIZE + 1

    if click[0] == 1:
        if not hint_button(game, col, row):
            game.try_move((col, row))
    elif click[2] == 1:
        game.alpha_beta_search()


def hint_button(game, col, row):
    if col == 10 and row == 1:
        game.hints = not game.hints
        if game.hints:
            game.alpha_beta_search()
        return True
    return False


def draw_pieces(game):
    state = game.board
    for i in range(state.size):
        for j in range(state.size):
            value = state.board[i][j]
            if value is 'O':
                draw_piece(i * TILE_SIZE, j * TILE_SIZE, 'white')
            elif value is 'X':
                draw_piece(i * TILE_SIZE, j * TILE_SIZE, 'black')


def draw_moves(game):
    moves   = game.board.valid_moves()
    optimal = game.get_optimal_move()
    for m in moves:
        if m == optimal and game.hints:
            draw_move((m[0] - 1) * TILE_SIZE, (m[1] - 1) * TILE_SIZE, True)
        else:
            draw_move((m[0] - 1) * TILE_SIZE, (m[1] - 1) * TILE_SIZE)


def draw_tile(posx, posy, t_type):
    posx += GLOBAL_OFFSET
    posy += GLOBAL_OFFSET
    borders = {
        'border_topleft':    (1, 0),     'border_top':           (2, 0),
        'border_topright':   (3, 0),     'border_left':          (1, 1),
        'border_right':      (3, 1),     'border_bottomleft':    (1, 2),
        'border_bottom':     (2, 2),     'border_bottomright':   (3, 2),
        'border_middle':     (2, 1)
    }

    if t_type is 'dark':
        DISPLAY.blit(TILES, (posx, posy), (0, TILE_SIZE, TILE_SIZE, TILE_SIZE))
    elif t_type is 'light':
        DISPLAY.blit(TILES, (posx, posy), (0, 0, TILE_SIZE, TILE_SIZE))
    elif t_type in borders:
        blit_tile(borders[t_type], (posx, posy))


def blit_tile(offset, pos):
    img_pos = (
        offset[0] * TILE_SIZE,
        offset[1] * TILE_SIZE,
        TILE_SIZE, TILE_SIZE
        )

    DISPLAY.blit(TILES, pos, img_pos)


def draw_piece(posx, posy, color):
    posx += GLOBAL_OFFSET
    posy += GLOBAL_OFFSET
    if color is 'black':
        DISPLAY.blit(PIECES, (posx, posy),
                     (TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
    elif color is 'white':
        DISPLAY.blit(PIECES, (posx, posy),
                     (2 * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))


def draw_move(posx, posy, is_optimal=False):
    posx += GLOBAL_OFFSET
    posy += GLOBAL_OFFSET
    if is_optimal:
        DISPLAY.blit(MOVES, (posx + ICON_SIZE // 2, posy + ICON_SIZE // 2),
                     (2 * ICON_SIZE, 2 * ICON_SIZE, ICON_SIZE, ICON_SIZE))
    else:
        DISPLAY.blit(MOVES, (posx + ICON_SIZE // 2, posy + ICON_SIZE // 2),
                     (ICON_SIZE, 2 * ICON_SIZE, ICON_SIZE, ICON_SIZE))


def draw_board(cols, rows):
    # Draw the board itself
    for i in range(cols):
        for j in range(rows):
            t_type = 'light' if (i+j) % 2 == 0 else 'dark'
            draw_tile(TILE_SIZE * i, TILE_SIZE * j, t_type)

    # Draw a frame around the board. First the corners, then the sides
    draw_tile(TILE_SIZE * -1, TILE_SIZE * -1, 'border_topleft')
    draw_tile(TILE_SIZE * cols, TILE_SIZE * -1, 'border_topright')
    draw_tile(TILE_SIZE * -1, TILE_SIZE * rows, 'border_bottomleft')
    draw_tile(TILE_SIZE * cols, TILE_SIZE * rows, 'border_bottomright')

    for i in range(rows):
        draw_tile(TILE_SIZE * i, TILE_SIZE * -1, 'border_top')
        draw_tile(TILE_SIZE * i, TILE_SIZE * rows, 'border_bottom')

    for j in range(cols):
        draw_tile(TILE_SIZE * -1, TILE_SIZE * j, 'border_left')
        draw_tile(TILE_SIZE * cols, TILE_SIZE * j, 'border_right')

    # Some extra background space for score etc
    for i in range(-1, rows + 1):
        draw_tile(TILE_SIZE * (cols + 1), TILE_SIZE * i, 'border_middle')
        draw_tile(TILE_SIZE * (cols + 2), TILE_SIZE * i, 'border_middle')

    # Add numbering for board
    abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    offset = FONT_SIZE // 2

    for i in range(rows):
        draw_text(abc[i], (TILE_SIZE * i + offset, -1 * TILE_SIZE + offset))

    for j in range(cols):
        draw_text(str(j + 1), (TILE_SIZE * -1 + offset, j * TILE_SIZE + offset))

if __name__ == '__main__':
    run_game()
