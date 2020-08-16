import pytest
from TicTacToe.Grid import Grid
from TicTacToe.Exceptions.TicTacToeExceptions import *


def test_GridInitialConditions():
    g = Grid(startingPlayer=1)
    assert g.currentPlayer == 1
    assert not g.win
    assert all(g.cells[i // 3][i % 3] == 0 for i in range(9))


def test_GridPlayFunctionsCorrectly():
    g = Grid(startingPlayer=1)

    p1Moves = [(0, 2), (1, 2), (2, 2), (2, 1), (1, 1)]
    p2Moves = [(2, 0), (1, 0), (0, 0), (0, 1), (1, 1)]

    g.play(1, p1Moves[0])
    assert not g.win

    g.play(2, p2Moves[0])
    assert not g.win

    g.play(1, p1Moves[1])
    assert not g.win

    g.play(2, p2Moves[1])
    assert not g.win

    g.play(1, p1Moves[2])
    assert g.win == 1


def test_GridPlayChecksBoundries():
    g = Grid(startingPlayer=1)
    with pytest.raises(InvalidGridIndexError):
        assert g.play(1, (-1, -1))

    # Make sure the turn didn't switch upon an error
    assert g.currentPlayer == 1

    with pytest.raises(InvalidGridIndexError):
        assert g.play(1, (1, -1))
    assert g.currentPlayer == 1

    with pytest.raises(InvalidGridIndexError):
        assert g.play(1, (-1, 1))
    assert g.currentPlayer == 1

    with pytest.raises(InvalidGridIndexError):
        assert g.play(1, (-1, 1))
    assert g.currentPlayer == 1

    with pytest.raises(InvalidGridIndexError):
        assert g.play(1, (-1, 1))
    assert g.currentPlayer == 1

    with pytest.raises(InvalidGridIndexError):
        assert g.play(1, (3, 1))
    assert g.currentPlayer == 1

    with pytest.raises(InvalidGridIndexError):
        assert g.play(1, (1, 3))
    assert g.currentPlayer == 1


def test_GridPlayChecksCurrentPlayer():
    g = Grid(startingPlayer=1)
    assert g.currentPlayer == 1

    with pytest.raises(WrongTurnError):
        assert g.play(2, (1, 2))
    assert g.lastPos is None

    g.play(1, (1, 2))
    assert g.lastPos[0] == 1 and g.lastPos[1] == 2
    assert g.lastPlayer == 1



