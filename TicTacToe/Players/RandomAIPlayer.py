from time import sleep
from random import choice
from TicTacToe.Players.Player import Player
from TicTacToe.Exceptions.AIExceptions import InvalidCellsError, NoPossibleMovesError


class RandomAIPlayer(Player):
    def __init__(self, playerNo, name=None, delay=None):
        self.delay = delay
        if name is None: name = f"Random AI #{playerNo}"
        super().__init__(playerNo, name)

    def getMove(self, cells):
        if len(cells) != 3 or any(len(cells[i]) != 3 for i in range(3)): raise InvalidCellsError
        possibleMoves = [(i // 3, i % 3) for i in range(9) if cells[i // 3][i % 3] == 0]
        if len(possibleMoves) == 0: raise NoPossibleMovesError
        if self.delay: sleep(self.delay)
        return choice(possibleMoves)

