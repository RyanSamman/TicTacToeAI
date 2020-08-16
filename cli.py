from threading import Thread
from multiprocessing import Process
from TicTacToe.Grid import Grid
from TicTacToe.util import getFormattedCells, saveData, displayData
from TicTacToe.Players.Player import Player
from TicTacToe.Players.AIPlayer import AIPlayer
from TicTacToe.Players.RandomAIPlayer import RandomAIPlayer
from TicTacToe.Exceptions.TicTacToeExceptions import GridError, AlreadyFilledError


if __name__ == '__main__':
    localGraph = Process(target=displayData)
    localGraph.start()

    game = Grid()
    key = {0: ' ', 1: 'X', 2: 'O'}
    playerList = [None, Player(playerNo=1), AIPlayer(playerNo=2)]

    print(f"Initial Player is {playerList[game.currentPlayer].name} ({key[game.currentPlayer]})")

    try:
        while not game.hasWon() and game.movesLeft:
            player = playerList[game.currentPlayer]
            move = player.getMove(game.cells)
            print(f"{player.name}'s Turn ({key[game.currentPlayer]}): played {move}")
            try:
                game.play(player.playerNo, move)
            except AlreadyFilledError:
                print(f"move {move} is Invalid")
                continue
            print(getFormattedCells(cells=game.cells, key=key))

        gameData = {
            'player1': playerList[1].__class__.__name__,
            'player2': playerList[2].__class__.__name__,
            'startingPlayer': playerList[game.lastPlayer].__class__.__name__,
            'moves': 9 - game.movesLeft,
            'win': True if game.win else False,
            'winner': playerList[game.lastPlayer].__class__.__name__ if game.win else '',
            'draw': False if game.win and game.movesLeft != 9 else True
        }

        if game.win:
            print(f"Game has ended in a win for {playerList[game.lastPlayer].name} ({key[game.currentPlayer]})")
        else:
            print("Game ended in a Draw!")
        Thread(target=saveData, args=(gameData,)).start()

    except GridError as e:
        print(f"{e.__class__.__name__}: {e}")
        print(game.cells)
        raise e
