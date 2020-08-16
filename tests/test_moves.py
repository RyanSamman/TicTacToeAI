from TicTacToe.util import getAllPossibleMoves


def test_generatesAllPossibleMoves():
    cellState = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    assert len(getAllPossibleMoves(cellState)) == 9


def test_generatesOneMove():
    cellState = [
        [1, 2, 1],
        [2, 0, 2],
        [1, 2, 1]
    ]

    moves = getAllPossibleMoves(cellState)
    assert len(moves) == 1
    assert (1, 1) in moves


def test_generatesManyMoves():
    cellState = [
        [1, 0, 1],
        [0, 2, 0],
        [1, 0, 1]
    ]

    moves = getAllPossibleMoves(cellState)
    assert len(moves) == 4
    assert (0, 1) in moves
    assert (1, 0) in moves
    assert (1, 2) in moves
    assert (2, 1) in moves
