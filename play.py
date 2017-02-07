#! /usr/bin/env python
# title           :play.py
# description     :Decides between 2 versions of reversi
# author          :andresthor
# date            :07-02-2017
# usage           :python play.py
# python_version  :3.5.2
# =============================================================================

# A veru crude way of chosing which version of the game to play. Just checks
# for the existance of pygame and what version of python the user has

import sys

print('\nREVERSI')
has_pygame = True
python_version = sys.version_info[0]

if python_version < 3:
    try:
        import pygame
    except ImportError, e:
        print('pygame not found - can only run cmd-line version.')
        has_pygame = False
else:
    print('Not running python3. GUI version will likely not run on python2.')

input = 0
while input not in [1, 2]:
    try:
        input = int(raw_input('\n1. Command-line version\n2. GUI version\n'))
    except:
        pass


if input == 1:
    execfile('cmd_line.py')
elif input == 2:
    if not has_pygame:
        print('You need to install pygame to play the GUI version!')
    else:
        execfile('gui.py')

print('Exiting program!')
