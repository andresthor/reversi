#! /usr/bin/env python

BLACK = 'X'
WHITE = 'O'
EMPTY = ' '


class ReversiBoard(object):

    def __init__(self, size):
        self.board = self.create_board(size, size)
        self.size  = size
        self.score = {BLACK: 0, WHITE: 0}
        self.turn  = None
        self.last  = None

        self.dirs  = [(-1, 0), ( 0, -1), ( 1, 0), ( 0,  1),
                      ( 1, 1), (-1, -1), (-1, 1), ( 1, -1)]

        self.init_pieces()

    def init_pieces(self):
        self.set_tiles([(4, 4), (5, 5)], WHITE)
        self.set_tiles([(4, 5), (5, 4)], BLACK)

        self.score = {BLACK: 2, WHITE: 2}
        self.turn  = BLACK
        self.last  = (4, 4)

    def create_board(self, cols, rows):
        return [[EMPTY for x in range(rows)] for x in range(cols)]

    def set_tiles(self, tiles, color):
        for t in tiles:
            self.set_tile(t, color)

    def set_tile(self, tile, color):
        if self.is_on_board(tile):
            self.board[tile[0] - 1][tile[1] - 1] = color

    def switch_turns(self):
        self.turn = BLACK if self.turn is WHITE else WHITE

    def is_on_board(self, tile):
        col, row  = tile[0] - 1, tile[1] - 1
        valid_col = col >= 0 and col < self.size
        valid_row = row >= 0 and row < self.size

        return valid_col and valid_row

    def valid_move(self, tile):
        if not self.is_on_board(tile):
            return False
        if not self.can_flip(tile):
            return False

        return True

    def can_flip(self, tile):
        if self.is_occupied(tile):
            return False

        for d in self.dirs:
            if self.flips_in_dir(tile, d) != []:
                return True

        return False

    def flips_in_dir(self, tile, direction):
        flips = []
        step  = add(tile, direction)

        found_ally  = False
        found_foe   = False

        while self.is_on_board(step) and self.get_tile(step) is not EMPTY:
            value = self.get_tile(step)
            if value is self.turn:
                found_ally = True
            elif value is self.opposite(self.turn) and not found_ally:
                flips.append(step)
                found_foe = True

            step = add(step, direction)

        if found_ally and found_foe:
            return flips
        else:
            return []

    def flips(self, tile):
        flips = []
        for d in self.dirs:
            flips += (self.flips_in_dir(tile, d))

        return flips

    def opposite(self, color):
        # Assumes the only colors sent in are BLACK or WHITE
        opposite = BLACK if color is WHITE else WHITE
        return opposite

    def is_occupied(self, tile):
        return self.get_tile(tile) is not EMPTY

    def get_tile(self, tile):
        return self.board[tile[0] - 1][tile[1] - 1]

    def do_move(self, tile):
        if self.valid_move(tile):
            self.set_tile(tile, self.turn)
            self.do_flips(tile)
            self.switch_turns()
            self.last = tile
            return True

        return False

    def do_flips(self, tile):
        self.set_tiles(self.flips(tile), self.turn)


def add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])


def print_board(board):
    '''Accepts a 2D list of variable dimensions and prints the contents'''

    cols, rows = len(board), len(board[0])
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
            out += '| ' + str(board[i][j]) + ' '
        print(out + '|')
        print(margin + space + cols * '+---' + '+')


def test_board():
    board = ReversiBoard(8)
    print_board(board.board)

if __name__ == '__main__':
    test_board()
