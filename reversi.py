#! /usr/bin/env python

import reversiboard as rb
import random
from copy import copy, deepcopy

BOARD_SIZE = 8
CUTOFF_DEPTH = 6
BLACK = 'X'
WHITE = 'O'
EMPTY = ' '

class Node(object):

    def __init__(self, data, parent=None, action=(-1, -1)):
        self.state    = data
        self.children = []
        self.parent   = parent
        self.value    = 0
        self.action   = action

    def add_child(self, data, action):
        child = Node(data, parent=self, action=action)
        self.children.append(child)
        return child


class Reversi(object):

    def __init__(self):
        self.board = rb.ReversiBoard(BOARD_SIZE)
        self.score = {BLACK: 2, WHITE: 2}
        self.size  = BOARD_SIZE
        self.root = None
        self.has_calculated = False

    def try_move(self, tile):
        self.score = self.board.score
        return self.board.do_move(tile)

    def alpha_beta_search(self):
        self.root = Node(self.board)
        self.root.value = self.max_value(self.root, -float('inf'), float('inf'), 0)
        self.calc_optimal_move()

        print('v = {}'.format(self.root.value))
        child_values = []
        for child in self.root.children:
            child_values.append(child.value)

        print('Children values: {}'.format(child_values))
        print('Optimal move: {}'.format(self.root.action))

    def optimal_moves(self):
        if self.root is None:
            return []
        optimal = []
        for child in self.root.children:
            if child.value == self.root.value:
                optimal.append(child.action)

        return optimal

    def update(self):
        if self.board.turn == BLACK:
            if not self.has_calculated:
                # self.alpha_beta_search()
                self.has_calculated = True
            return

        self.has_calculated = False
        self.alpha_beta_search()
        self.try_move(self.root.action)

    def calc_optimal_move(self):
        moves = self.optimal_moves()
        if moves != []:
            self.root.action = random.choice(moves)

    def get_optimal_move(self):
        if self.root is not None:
            return self.root.action
        else:
            return None

    def result(self, state, action):
        new_state = deepcopy(state)
        new_state.do_move(action)
        return new_state

    def actions(self, state):
        return state.valid_moves()

    def eval(self, state):
        max_score = state.score[self.board.turn]
        min_score = state.score[state.opposite(self.board.turn)]

        p = 100 * (max_score - min_score) / (max_score + min_score)

        corners = {BLACK: 0, WHITE: 0, EMPTY: 0}
        corner_list = [(1, 1), (1, 8), (8, 1), (8, 8)]
        for corner in corner_list:
            corners[state.get_tile(corner)] += 1

        max_corn = corners[self.board.turn]
        min_corn = corners[state.opposite(self.board.turn)]
        c = 0
        if (corners[BLACK] + corners[WHITE] != 0):
            c = 100 * (max_corn - min_corn) / (max_corn + min_corn)

        return p + c

    def max_value(self, node, alpha, beta, depth):
        depth += 1
        if self.cut_off_test(node.state, depth):
            return self.eval(node.state)

        v = -float('inf')
        for action in self.actions(node.state):
            child = node.add_child(self.result(node.state, action), action)
            v = max(v, self.min_value(child, alpha, beta, depth))
            child.value = v
            if v >= beta:
                return v
            alpha = max(alpha, v)

        return v

    def min_value(self, node, alpha, beta, depth):
        depth += 1
        if self.cut_off_test(node.state, depth):
            return self.eval(node.state)

        v = -float('inf')
        for action in self.actions(node.state):
            child = node.add_child(self.result(node.state, action), action)
            v = max(v, self.max_value(child, alpha, beta, depth))
            child.value = v
            if v <= alpha:
                return v
            beta = min(beta, v)

        return v

    def cut_off_test(self, state, depth):
        return depth >= CUTOFF_DEPTH or self.terminal_test(state)

    def terminal_test(self, state):
        return state.board_full() or state.valid_moves == []


if __name__ == '__main__':
    r = Reversi()
