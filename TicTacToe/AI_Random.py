from random import choice
from TicTacToe.Exceptions import InvalidCellsError, NoPossibleMovesError


def makeRandomMove(cells):
    if len(cells) != 3 or any(len(cells[i]) != 3 for i in range(3)): raise InvalidCellsError
    possibleMoves = [(i // 3, i % 3) for i in range(9) if cells[i // 3][i % 3] == 0]
    if len(possibleMoves) == 0: raise NoPossibleMovesError
    return choice(possibleMoves)
