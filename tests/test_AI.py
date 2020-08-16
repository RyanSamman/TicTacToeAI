from TicTacToe.Grid import Grid
from TicTacToe.util import getFormattedCells, getAllPossibleMoves, checkWin
from TicTacToe.Exceptions.TicTacToeExceptions import AlreadyFilledError
from TicTacToe.Players.RandomAIPlayer import RandomAIPlayer
from TicTacToe.Players.AIPlayer import AIPlayer


def test_LosesIfNotMiddle():
    playerList = [None, RandomAIPlayer(playerNo=1), AIPlayer(playerNo=2)]
    game = Grid(startingPlayer=2)

    while not game.hasWon() and game.movesLeft:
        if game.currentPlayer == 1 and game.movesLeft == 8:
            game.play(game.currentPlayer, (1, 0))
            continue

        player = playerList[game.currentPlayer]
        move = player.getMove(game.cells)
        game.play(player.playerNo, move)

    assert checkWin(game.cells) == 2  # Minimax player will always win


def test_DrawsAgainstSelf():
    playerList = [None, AIPlayer(playerNo=1), AIPlayer(playerNo=2)]
    game = Grid(startingPlayer=2)

    while not game.hasWon() and game.movesLeft:
        player = playerList[game.currentPlayer]
        move = player.getMove(game.cells)
        game.play(player.playerNo, move)

    assert checkWin(game.cells) == 0  # Should always draw


# If the AI processes differently this should fail
def test_States():
    playerList = [None, None, AIPlayer(playerNo=2)]
    game = Grid(startingPlayer=1)
    playerPlays = [(0, 0), (0, 1), (2, 0), (1, 2), (2, 2)]
    p1 = 0

    while not game.hasWon() and game.movesLeft:
        if game.currentPlayer == 1:
            game.play(game.currentPlayer, playerPlays[p1])
            p1 += 1
            continue

        player = playerList[game.currentPlayer]
        move = player.getMove(game.cells)
        game.play(player.playerNo, move)

        if game.currentPlayer == 2 and p1 == 0:
            assert game.cells[1][1] == 2

        if game.currentPlayer == 2 and p1 == 1:
            assert game.cells[0][2] == 2

        if game.currentPlayer == 2 and p1 == 2:
            assert game.cells[1][0] == 2

        if game.currentPlayer == 2 and p1 == 4:
            assert game.cells[2][1] == 2

    assert checkWin(game.cells) == 0
