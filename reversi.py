#! /usr/bin/env python

import reversiboard as rb
from copy import copy, deepcopy

BOARD_SIZE = 8
CUTOFF_DEPTH = 6


class Node(object):

    def __init__(self, data, parent=None):
        self.state    = data
        self.children = []
        self.parent   = parent
        self.value    = 0

    def add_child(self, data):
        child = Node(data, parent=self)
        self.children.append(child)
        return child


class Reversi(object):

    def __init__(self):
        self.board = rb.ReversiBoard(BOARD_SIZE)
        self.score = {'black': 2, 'white': 2}
        self.size  = BOARD_SIZE
        self.search_tree = None

    def try_move(self, tile):
        return self.board.do_move(tile)


if __name__ == '__main__':
    r = Reversi()
