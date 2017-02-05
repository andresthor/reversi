#! /usr/bin/env python

from constants import BLACK, WHITE, EMPTY


def add(t1, t2):
    '''A simple function that adds together two tuples'''
    return (t1[0] + t2[0], t1[1] + t2[1])


class ReversiBoard(object):
    '''Creates a board of reversi and keeps track of pieces and legal moves'''

    def __init__(self, size):
        self.board = self.create_board(size, size)
        self.size  = size
        self.score = {BLACK: 0, WHITE: 0}
        self.turn  = None
        self.last  = None

        # Move directions in tuple form
        self.dirs  = [(-1, 0), ( 0, -1), ( 1, 0), ( 0,  1),
                      ( 1, 1), (-1, -1), (-1, 1), ( 1, -1)]

        self.init_pieces()

    def init_pieces(self):
        '''Initializes the board with the classic setup of 2x2 pieces'''
        self.set_tiles([(4, 4), (5, 5)], WHITE)
        self.set_tiles([(4, 5), (5, 4)], BLACK)

        self.score = {BLACK: 2, WHITE: 2}
        self.turn  = BLACK
        self.last  = (4, 4)

    def create_board(self, cols, rows):
        '''Creates a 2d array with EMPTY slots'''
        return [[EMPTY for x in range(rows)] for x in range(cols)]

    def set_tiles(self, tiles, color):
        '''Takes a list of tiles (tuples) and sets them to "color"'''
        for t in tiles:
            self.set_tile(t, color)

    def set_tile(self, tile, color):
        '''Sets a single tile (tuple) to "color"'''
        if self.is_on_board(tile):
            self.board[tile[0] - 1][tile[1] - 1] = color

    def switch_turns(self):
        '''Switches the active player'''
        self.turn = BLACK if self.turn is WHITE else WHITE

    def is_on_board(self, tile):
        '''Returns True if the tile is a valid (column, row) tuple'''
        col, row  = tile[0] - 1, tile[1] - 1
        valid_col = col >= 0 and col < self.size
        valid_row = row >= 0 and row < self.size

        return valid_col and valid_row

    def valid_move(self, tile, color=None):
        '''Returns True if the move is legal'''
        if color is None:
            color = self.turn
        if not self.is_on_board(tile):
            return False
        if not self.can_flip(tile, color):
            return False

        return True

    def can_flip(self, tile, color):
        '''Returns True if setting tile to color will cause some piece(s) to be
           flipped.
        '''

        if self.is_occupied(tile):
            return False

        for d in self.dirs:
            if self.flips_in_dir(tile, d, color) != []:
                return True

        return False

    def flips_in_dir(self, tile, direction, color):
        '''Iterates from tile in direction, and determines if setting the tile
           to color will cause a piece to be flipped in that directiona.
           Returns a list of the flippable tiles.
        '''

        flips = []
        step  = add(tile, direction)
        found_ally, found_foe = False, False

        while self.is_on_board(step) and self.get_tile(step) is not EMPTY:
            value = self.get_tile(step)
            if value is color:
                found_ally = True
            elif value is self.opposite(color) and not found_ally:
                flips.append(step)
                found_foe = True

            step = add(step, direction)

        if found_ally and found_foe:
            return flips
        else:
            return []

    def flips(self, tile, color):
        '''Checks all directions for flippable tiles, assuming tile is set to
           color. Returns a list of the flippable tiles.
        '''

        flips = []
        for d in self.dirs:
            flips += (self.flips_in_dir(tile, d, color))

        return flips

    def valid_moves(self, color=None):
        '''Returns a list of legal moves for color'''
        if color is None:
            color = self.turn
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.valid_move((i + 1, j + 1), color):
                    moves.append((i + 1, j + 1))

        return moves

    def opposite(self, color):
        '''Returns the opposite color. Assumes the only colors sent in are BLACK
           or WHITE.
        '''

        opposite = BLACK if color is WHITE else WHITE
        return opposite

    def is_occupied(self, tile):
        '''Returns True if the tile is already occupied by a piece'''
        return self.get_tile(tile) is not EMPTY

    def get_tile(self, tile):
        '''Returns the value at the specified tile'''
        return self.board[tile[0] - 1][tile[1] - 1]

    def do_move(self, tile):
        '''Makes a move at the selected tile, with the active player, if the
           move is valid. Then calculates score and switches turns.
        '''

        if self.valid_move(tile):
            self.set_tile(tile, self.turn)
            self.do_flips(tile)
            self.switch_turns()
            self.last = tile
            self.calc_score()
            return True

        return False

    def do_flips(self, tile, color=None):
        '''Carries out the flips required for the specified move.'''
        if color is None:
            color = self.turn
        self.set_tiles(self.flips(tile, color), self.turn)

    def board_full(self):
        '''Returns True if the board is full.'''
        return sum(x.count(EMPTY) for x in self.board) == 0

    def calc_score(self):
        '''Calculates the score and stores in self.score'''
        self.score[BLACK] = sum(x.count(BLACK) for x in self.board)
        self.score[WHITE] = sum(x.count(WHITE) for x in self.board)

    def ascii(self):
        '''Prints out an ASCII version of the current board.'''

        cols, rows = len(self.board), len(self.board[0])
        margin = '  ' if rows < 10 else '   '

        # Print top
        top = margin + ' '
        for i in range(cols):
            space = ' ' if i < 9 else ''
            top += ' ' + str(i+1) + '.' + space
        print(top)
        print(margin + ' ' + cols * '+---' + '+')

        # Print rows
        for j in range(rows):
            space = ' ' if j < 9 else ''
            out = str(j+1) + '.' + space
            for i in range(cols):
                out += '| ' + str(self.board[i][j]) + ' '
            print(out + '|')
            print(margin + space + cols * '+---' + '+')
