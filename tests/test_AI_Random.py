import pytest
import TicTacToe.Exceptions.AIExceptions as AIExceptions
from TicTacToe.Players.RandomAIPlayer import RandomAIPlayer


def test_rejectsInvalidInput():

    with pytest.raises(AIExceptions.InvalidCellsError):
        assert RandomAIPlayer.getMove([])

    with pytest.raises(AIExceptions.InvalidCellsError):
        assert RandomAIPlayer.getMove([1, 2])

    with pytest.raises(AIExceptions.InvalidCellsError):
        assert RandomAIPlayer.getMove([[1, 2, 3], [1, 2]])

    with pytest.raises(AIExceptions.InvalidCellsError):
        assert RandomAIPlayer.getMove([[], [], []])


def test_recognizesFullBoard():
    with pytest.raises(AIExceptions.NoPossibleMovesError):
        assert RandomAIPlayer.getMove([[1, 1, 1], [1, 1, 1], [1, 1, 1]])


def test_functionsAsIntended():
    cellState = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    moveCount = 0
    while True:
        try:
            y, x = RandomAIPlayer.getMove(cellState)
            cellState[y][x] = 1
            moveCount += 1
        except AIExceptions.NoPossibleMovesError:
            assert moveCount == 9
            break
    assert all(cellState[i // 3][i % 3] == 1 for i in range(9))
