from random import choice
from TicTacToe.Exceptions import InvalidCellsError, NoPossibleMovesError


def makeRandomMove(cells):
    if any(len(cells[i]) != 3 for i in range(3)): raise InvalidCellsError
    possibleMoves = [(i // 3, i % 3) for i in range(9) if cells[i // 3][i % 3] == 0]
    if len(possibleMoves) == 0: raise NoPossibleMovesError
    return choice(possibleMoves)


if __name__ == '__main__':
    cellState = [
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ]

    moveCount = 0
    while True:
        try:
            y, x = makeRandomMove(cellState)
            print(f"Chosen move: ({y}, {x})")
            cellState[y][x] = 1
            moveCount += 1
        except NoPossibleMovesError:
            break
    print("Total moves:", moveCount)
    assert moveCount == 9
    print(cellState)