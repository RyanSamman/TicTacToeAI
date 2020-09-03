from time import sleep
from threading import Thread
from TicTacToe import Player
from functools import reduce
from TicTacToe.util import checkWin, getAllPossibleMoves
from TicTacToe.Exceptions.AIExceptions import NoPossibleMovesError, AIError


class AIPlayer(Player):
    def __init__(self, playerNo, name=None, delay=0):
        self.delay = delay
        if name is None: name = f"Minmax AI #{playerNo}"
        self.maximizing, self.minimizing = (1, 2) if playerNo == 1 else (2, 1)
        super().__init__(playerNo, name)

    def getMove(self, cells):
        sleepThread = Thread(target=lambda: sleep(self.delay))
        sleepThread.start()

        moves = getAllPossibleMoves(cells)
        if len(moves) == 9: return 0, 0  # Pre-computed first move to avoid going through all 255,168 possible states
        if len(moves) == 0: raise NoPossibleMovesError

        move = max(moves, key=lambda m: self.getMoveScore(m, cells, self.maximizing))

        sleepThread.join()  # Ensure it takes at least "self.delay" seconds to run
        return move

    def getMoveScore(self, move, cells, player, recursionDepth=0):
        cells[move[0]][move[1]] = player # Apply move

        boardWinState = checkWin(cells)
        moves = getAllPossibleMoves(cells)

        if boardWinState is not None:
            scoreMap = {
                0: 0, # Draw
                self.maximizing: 10 - recursionDepth, # AI Win
                self.minimizing: -10 + recursionDepth # Opponent Win
            }
            score = scoreMap[boardWinState]
        elif player == self.maximizing:
            score = min(self.getMoveScore(m, cells, self.minimizing, recursionDepth + 1) for m in moves)
        elif player == self.minimizing:
            score = max(self.getMoveScore(m, cells, self.maximizing, recursionDepth + 1) for m in moves)
        else:
            raise AIError(f"{player} is an invalid player value!")

        cells[move[0]][move[1]] = 0 # Revert move
        return score
