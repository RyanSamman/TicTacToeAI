from TicTacToe.util import checkWin


def test_GridWinState():
    cells = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    assert checkWin(cells) is None

    cells = [
        [1, 2, 0],
        [1, 2, 0],
        [1, 0, 0],
    ]
    assert checkWin(cells) == 1

    cells = [
        [2, 1, 0],
        [2, 1, 0],
        [0, 1, 0],
    ]
    assert checkWin(cells) == 1

    cells = [
        [2, 0, 1],
        [2, 0, 1],
        [0, 0, 1],
    ]
    assert checkWin(cells) == 1

    cells = [
        [0, 2, 0],
        [0, 2, 0],
        [1, 1, 1],
    ]
    assert checkWin(cells) == 1

    cells = [
        [0, 2, 0],
        [1, 1, 1],
        [0, 2, 0],
    ]
    assert checkWin(cells) == 1

    cells = [
        [1, 1, 1],
        [0, 2, 0],
        [0, 2, 0],
    ]
    assert checkWin(cells) == 1

    cells = [
        [0, 1, 2],
        [0, 2, 0],
        [2, 1, 0],
    ]
    assert checkWin(cells) == 2

    cells = [
        [2, 1, 0],
        [0, 2, 0],
        [0, 1, 2],
    ]
    assert checkWin(cells) == 2

    cells = [
        [2, 1, 2],
        [2, 2, 1],
        [1, 2, 1],
    ]
    assert checkWin(cells) == 0
