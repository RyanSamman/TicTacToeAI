from time import sleep
from random import choice
from threading import Thread
from TicTacToe.util import getAllPossibleMoves
from TicTacToe.Players.Player import Player
from TicTacToe.Exceptions.AIExceptions import InvalidCellsError, NoPossibleMovesError


class RandomAIPlayer(Player):
    def __init__(self, playerNo, name=None, delay=0):
        self.delay = delay
        if name is None: name = f"Random AI #{playerNo}"
        super().__init__(playerNo, name)

    def getMove(self, cells):
        sleepThread = Thread(target=lambda: sleep(self.delay))
        sleepThread.start()

        if len(cells) != 3 or any(len(cells[i]) != 3 for i in range(3)): raise InvalidCellsError
        possibleMoves = getAllPossibleMoves(cells)
        if len(possibleMoves) == 0: raise NoPossibleMovesError
        if self.delay: sleep(self.delay)

        sleepThread.join()
        return choice(possibleMoves)
