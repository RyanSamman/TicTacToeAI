from time import sleep
from threading import Thread
from TicTacToe import Player
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

        # TODO: Refactor code to
        moves = getAllPossibleMoves(cells)
        if len(moves) == 9: return 0, 0  # Pre-computed first move to avoid going through all 255,168 possible states
        if len(moves) == 0: raise NoPossibleMovesError

        bestScore = -10  # Worst possible state is a -9
        move = (-5, -5)  # Default move, an exception will be raised if it somehow manages to pass through
        for i, j in moves:
            cells[i][j] = self.maximizing
            score = self.getMoveScore(cells, self.minimizing, 1)
            cells[i][j] = 0
            if score > bestScore:
                bestScore = score
                move = (i, j)

        sleepThread.join()  # Ensure it takes at least "self.delay" seconds to run
        return move

    def getMoveScore(self, cells, player, recursionDepth):
        """
        ~ Minimax Algorithm

        Reference:
            - Wikipedia - https://en.wikipedia.org/wiki/Minimax

        :paaram move: Move to be scored
        :param cells: Cells to be inspected
        :param player: Minimizing player or Maximizing player
        :param recursionDepth: The current recursion depth
        :return: A heuristic or 'score'  from -9 to 9
        """
        boardWinState = checkWin(cells)  # 0 if tie, 1 and 2 if, p1 and p2, respectively won, else, None
        moves = getAllPossibleMoves(cells)

        if boardWinState is not None:
            score = {0: 0, self.maximizing: 10 - recursionDepth, self.minimizing: -10 + recursionDepth}
            return score[boardWinState]

        elif player == self.maximizing:
            bestScore = -10  # Worst possible score (in ths scenario) is -9
            for i, j in moves:
                cells[i][j] = self.maximizing
                score = self.getMoveScore(cells, self.minimizing, recursionDepth + 1)
                cells[i][j] = 0
                bestScore = max(bestScore, score)
            return bestScore

        elif player == self.minimizing:
            worstScore = 10  # Best possible score (in ths scenario) is 9
            for i, j in moves:
                cells[i][j] = self.minimizing
                score = self.getMoveScore(cells, self.maximizing, recursionDepth + 1)
                cells[i][j] = 0
                worstScore = min(worstScore, score)
            return worstScore

        else:
            raise AIError(f"{player} is an invalid player value!")
