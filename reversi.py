#! /usr/bin/env python
# title           :reversi.py
# description     :A class that handles a game of reversi, complete with AI
# author          :andresthor
# date            :05-02-2017
# python_version  :3.5.2
# =============================================================================

import reversiboard as rb
from constants import BLACK, WHITE, EMPTY, BOARD_SIZE, CUTOFF_DEPTH
import random
from copy import deepcopy


class Node(object):
    '''
        Basic node object to build the search tree used in the Reversi class
    '''

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
    '''
        A game of reversi that uses minimax search with alpha-beta pruning

        Initializes a 8x8 board with typical starting pieces. The computer
        plays as WHITE while the player is BLACK.
        The player should make his moves with try_move((column, row)).
        Tips can be turned on with toggle_hints
    '''

    def __init__(self):
        self.board = rb.ReversiBoard(BOARD_SIZE)
        self.score = {BLACK: 2, WHITE: 2}
        self.size  = BOARD_SIZE
        self.root  = None
        self.hints = False

        self.has_calculated = False
        self.game_over      = False

    def try_move(self, tile):
        '''Tries to make a move at (tile[0], tile[1]) with the current board'''

        self.score = self.board.score
        return self.board.do_move(tile)

    def toggle_hints(self):
        '''Toggles the use of the alpha-beta-search when it's the player's turn.
           If True, the optimal move can then be fetched with get_optimal_move.
        '''

        self.hints = not self.hints

    def alpha_beta_search(self):
        '''Runs a minimax search with alpha-beta pruning. The optimal move is
           then retrievable with get_optimal_move
        '''

        self.root = Node(self.board)
        self.root.value = self.max_value(self.root, -float('inf'), float('inf'), 0)
        self.calc_optimal_move()

    def calc_optimal_move(self):
        '''Selects an optimal move after an alpha-beta search. If there are
           multiple moves with the same minimax value, a random one is selected
        '''

        moves = self.optimal_moves()
        if moves != []:
            self.root.action = random.choice(moves)

    def get_optimal_move(self):
        '''Returns the current optimal move'''

        if self.root is not None:
            return self.root.action
        else:
            return None


    def optimal_moves(self):
        '''Returns a list of all optimal moves'''

        if self.root is None:
            return []
        optimal = []
        for child in self.root.children:
            if child.value == self.root.value:
                optimal.append(child.action)

        return optimal

    def update(self):
        '''Updates the game.
           Runs the required search when it's the computer's turn. Also runs the
           search for the player if hints are turned on.
        '''

        if self.game_over:
            return

        # Is the game over or does the current player have no moves available?
        if self.board.board_full():
            self.game_over = True
        elif self.board.valid_moves() == []:
            # Current player has no moves available
            other_player = self.board.opposite(self.board.turn)
            if self.board.valid_moves(other_player) == []:
                # Both players are our of moves
                self.game_over = True
            # The other player has moves available, switching turns
            self.board.switch_turns()

        # It's the player's turn
        if self.board.turn == BLACK:
            # Do we need to do the alpha-beta search?
            if not self.has_calculated:
                if self.hints:
                    self.alpha_beta_search()
                self.has_calculated = True
            return

        # It's the computer's turn
        self.has_calculated = False
        self.alpha_beta_search()
        self.try_move(self.root.action)

    def result(self, state, action):
        '''Returns the transition model that defines the results of an
           action/move
        '''

        new_state = deepcopy(state)
        new_state.do_move(action)
        return new_state

    def actions(self, state):
        '''Returns all valid actions for the specified state'''
        return state.valid_moves()

    def eval(self, state):
        '''Heuristic that tries to determine the utility of the state.

           Uses three statistics to compute a value:
               1. Score for the active player in state
               2. How many corners have been occupied by the players
               3. The mobility, i.e. number of moves available to both players
        '''

        weights = {'score': 500, 'corners': 100, 'mobility': 300}

        # 1. Current score
        max_score = state.score[self.board.turn]
        min_score = state.score[state.opposite(self.board.turn)]
        p = self._eval(max_score, min_score, weights['score'])

        # Number of occupied corners
        corners = {BLACK: 0, WHITE: 0, EMPTY: 0}
        corner_list = [(1, 1), (1, 8), (8, 1), (8, 8)]
        for corner in corner_list:
            corners[state.get_tile(corner)] += 1

        max_corn = corners[self.board.turn]
        min_corn = corners[state.opposite(self.board.turn)]
        c = self._eval(max_corn, min_corn, weights['corners'])

        # Mobility of players
        max_mob = len(state.valid_moves(color=self.board.turn))
        min_mob = len(state.valid_moves(color=state.opposite(self.board.turn)))
        m = self._eval(max_mob, min_mob, weights['mobility'])

        return p + c + m

    def _eval(self, max_p, min_p, weight):
        '''Sub-method to eval'''

        p = 0
        if (max_p + min_p != 0):
            p = weight * (max_p - min_p) / (max_p + min_p)

        return p

    def max_value(self, node, alpha, beta, depth):
        '''Performs a minimax search with alpha-beta pruning. Returns the action
           corresponding to the max of the min_value.
           Search ends when reaching a terminal state or when reaching the
           cutoff depth
        '''

        depth += 1
        if self.cut_off_test(node.state, depth, node.state.turn):
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
        '''Performs a minimax search with alpha-beta pruning. Returns the action
           corresponding to the min of the max_value.
           Search ends when reaching a terminal state or when reaching the
           cutoff depth
        '''

        depth += 1
        if self.cut_off_test(node.state, depth, node.state.turn):
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

    def cut_off_test(self, state, depth, color):
        '''Returns True if the cutoff depth has been reached, or if the game
            has reached a terminal state.
        '''

        return depth >= CUTOFF_DEPTH or self.terminal_test(state, color)

    def terminal_test(self, state, color):
        '''Checks if a terminal state has been reached (no moves)'''
        return state.board_full() or state.valid_moves(color) == []


if __name__ == '__main__':
    r = Reversi()
