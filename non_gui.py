#! /usr/bin/env python
# title           :non_gui.py
# description     :Runs a cmd-line version of Reversi
# author          :andresthor
# date            :05-02-2017
# usage           :python non_gui.py
# python_version  :3.5.2
# =============================================================================

from reversi import Reversi
from constants import BLACK, WHITE
from cmd import Cmd

INVALID_INPUT = '\n'.join(['Input should be in the form x#',
                           'where x is a lowercase letter between a-h',
                           'and # is a number between 1-8'])

NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8]
LETTERS = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
LET_LST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


class ReversiCMD(Cmd):
    '''An implementation of the Reversi game using a command line interface

       Prints out an ascii verison of the game state and accepts input in the
       form of "move a1", "move h8" etc.
       Player controls Black, Computer controls White
    '''

    prompt = '$: '

    def __init__(self, reversi):
        Cmd.__init__(self)
        self.reversi = reversi

    def cmdloop(self):
        # print(intro)
        self.print_board()
        print('Write help to get information on the available commands')
        return Cmd.cmdloop(self)

    def postcmd(self, stop, line):
        if self.reversi.terminal_test(self.reversi.board,
	                              self.reversi.board.turn):
            self.print_end_game()
            self.do_quit('')
        return Cmd.postcmd(self, stop, line)

    def do_quit(self, line):
        '''Ends the program'''
        return True

    def do_move(self, line):
        if len(line) != 2:
            print(INVALID_INPUT)
            return

        number = self.contains(line, NUMBERS)
        letter = self.contains(line, LETTERS)

        if not (letter and number):
            print(INVALID_INPUT)
            return

        if self.reversi.try_move((LETTERS[letter], number)):
            self.print_board()
            self.print_info((letter, number), BLACK)
            self.reversi.update()
            self.print_board()
            self.print_info(self.get_last_computer_move(), WHITE)
        else:
            print('Invalid move: {}{}'.format(letter, number))

    def help_move(self):
        print('move [x#] OR move [#x]\nWhere x is a letter a-h and # a nbr 1-8')

    def do_hint(self, line):
        '''Gives the player an optimal move hint (alpha-beta search)'''
        if not self.reversi.hints:
            self.reversi.toggle_hints()
        self.reversi.alpha_beta_search()

        move = self.reversi.get_optimal_move()
        print('Optimal move: {}{}'.format(LET_LST[move[0] - 1], move[1]))

    def do_cheat(self, line):
	'''Make optimal move'''
        if not self.reversi.hints:
            self.reversi.toggle_hints()
        self.reversi.alpha_beta_search()

	move = self.reversi.get_optimal_move()
	self.do_move(LET_LST[move[0] - 1] + str(move[1]))

    def do_show(self, line):
        '''Prints out the current game state'''
        self.print_board()
        self.print_info(self.get_last_computer_move(), self.reversi.board.turn)

    def do_AI(self, line):
        '''AI better OR AI worse\nMake AI better or worse'''
        if line == 'better':
            self.reversi.cutoff_depth += 1
        elif line == 'worse':
            self.reversi.cutoff_depth -= 1

	if self.reversi.cutoff_depth < 2:
	    self.reversi.cutoff_depth = 2

    def get_last_computer_move(self):
        move = self.reversi.board.last
        move = (LET_LST[move[0] - 1], move[1])
        return move

    def print_board(self):
        print('')
        self.reversi.board.ascii()

    def print_info(self,  move, player):
        turn_time = 0
	if player is BLACK:
            print('Your move was {}{}'.format(move[0], move[1]))
            turn_time = self.reversi.black_last
        elif player is WHITE:
            print("The computer's move was {}{}".format(move[0], move[1]))
	    turn_time = self.reversi.white_last

	print('Move took {:.3f}s'.format(turn_time))
        score = self.reversi.score
        print('Score is (black/white): {}/{}\n'.format(score[BLACK], score[WHITE]))

    def contains(self, line, items):
        for i in items:
            if str(i) in line:
                return i

        return False

    def print_end_game(self):
        score = self.reversi.score
        winner = 'Nobody - Draw'
        if score[BLACK] > score[WHITE]:
            winner = 'Black'
        elif score[WHITE] > score[BLACK]:
            winner = 'White'

        print('Game Over!')
        print('Time used (black/white): {:.3f}/{:.3f}'
	      .format(self.reversi.black_time, self.reversi.white_time))
        print('Score (black/white): {}/{}'.format(score[BLACK], score[WHITE]))
        print('Winner: {}'.format(winner))


if __name__ == '__main__':
    reversi = Reversi()
    ReversiCMD(reversi).cmdloop()
