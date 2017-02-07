# constants.py

# Colors/Pieces
WHITE = 'O'
BLACK = 'X'
EMPTY = ' '

# Game specific
BOARD_SIZE    = 8
CUTOFF_DEPTH  = 4
CUTOFF_TIME   = 5.0
CUTOFF_MARGIN = 0.3

# GUI
TILE_SIZE      = 32                     # Tiles used as base to build board
ICON_SIZE      = TILE_SIZE // 2
DISPLAY_WIDTH  = 12 * TILE_SIZE         # Display is wider than board
DISPLAY_HEIGHT = 10 * TILE_SIZE
GLOBAL_OFFSET  = TILE_SIZE              # Offset to include boarder around board
FONT_SIZE      = TILE_SIZE // 2
SCORE_POS_X    = 9 * TILE_SIZE
SCORE_POS_Y    = 1 * TILE_SIZE
