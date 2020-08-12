import pytest
from TicTacToe.AI_Random import makeRandomMove
from TicTacToe.Exceptions import NoPossibleMovesError, InvalidCellsError


def test_rejectsInvalidInput():
    with pytest.raises(InvalidCellsError):
        assert makeRandomMove([])

    with pytest.raises(InvalidCellsError):
        assert makeRandomMove([1, 2])

    with pytest.raises(InvalidCellsError):
        assert makeRandomMove([[1, 2, 3], [1, 2]])

    with pytest.raises(InvalidCellsError):
        assert makeRandomMove([[], [], []])


def test_recognizesFullBoard():
    with pytest.raises(NoPossibleMovesError):
        assert makeRandomMove([[1, 1, 1], [1, 1, 1], [1, 1, 1]])


def test_functionsAsIntended():
    cellState = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    moveCount = 0
    while True:
        try:
            y, x = makeRandomMove(cellState)
            cellState[y][x] = 1
            moveCount += 1
        except NoPossibleMovesError:
            assert moveCount == 9
            break
    assert all(cellState[i // 3][i % 3] == 1 for i in range(9))
    print(cellState)

