from random import randint
from TicTacToe.util import checkWin
from TicTacToe.Exceptions.TicTacToeExceptions import *


class Grid:
    def __init__(self, startingPlayer=None):
        self.restartGrid(startingPlayer)

    def restartGrid(self, startingPlayer=None):
        if startingPlayer is None: startingPlayer = randint(1, 2)
        self.startingPlayer = startingPlayer
        self.cells = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.currentPlayer = startingPlayer
        self.win = False
        self.movesLeft = 9
        self.lastPos = None

    def play(self, player, move):
        if self.win or not self.movesLeft: raise GameEndedError()
        if self.currentPlayer != player: raise WrongTurnError(self.currentPlayer)
        self.setCell(y=move[0], x=move[1])
        self.movesLeft -= 1
        self.lastPos = move
        self.lastPlayer = player
        self.switchToNextPlayer()
        self.hasWon()  # Update self.win

        return self.cells

    def setCell(self, y, x):
        if not (3 > x >= 0 and 3 > y >= 0): raise InvalidGridIndexError(y, x)
        if self.cells[y][x]: raise AlreadyFilledError(y, x)
        self.cells[y][x] = self.currentPlayer

    def switchToNextPlayer(self):
        self.currentPlayer = 2 if self.currentPlayer == 1 else 1
        return self.currentPlayer

    def hasWon(self):
        if self.lastPos is None: return False  # If the game hasn't started, nobody has won
        self.win = checkWin(self.cells)
        return self.win
