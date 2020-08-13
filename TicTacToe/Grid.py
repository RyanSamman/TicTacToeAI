from random import randint
from TicTacToe.Exceptions.TicTacToeExceptions import *
from TicTacToe.Players.RandomAIPlayer import RandomAIPlayer
from TicTacToe.Players.Player import Player


class Grid:
    def __init__(self, startingPlayer=None):
        self.restart(startingPlayer)

    def restart(self, startingPlayer=None):
        if startingPlayer is None: startingPlayer = randint(1, 2)
        self.cells = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.currentPlayer = startingPlayer
        self.win = False
        self.movesLeft = 9
        self.lastPos = None

    def play(self, player, move):
        if self.win or not self.movesLeft: raise GameEndedError()
        if self.currentPlayer != player: raise WrongTurnError(self.currentPlayer)
        self.setCell(y=move[0], x=move[1])
        self.movesLeft -= 1
        self.lastPos = move
        self.lastPlayer = player
        self.switchToNextPlayer()
        self.hasWon()

        return self.cells

    def setCell(self, y, x):
        if not (3 > x >= 0 and 3 > y >= 0): raise InvalidGridIndexError(x, y)
        if self.cells[y][x]: raise AlreadyFilledError(x, y)
        self.cells[y][x] = self.currentPlayer

    def switchToNextPlayer(self):
        self.currentPlayer = 2 if self.currentPlayer == 1 else 1
        return self.currentPlayer

    def getFormattedCells(self, cells=None, key=None):
        if cells is None: cells = self.cells
        f = cells
        formattedCells = (
            f"{f[0][0]}|{f[0][1]}|{f[0][2]}\n"
            f"{f[1][0]}|{f[1][1]}|{f[1][2]}\n"
            f"{f[2][0]}|{f[2][1]}|{f[2][2]}\n"
        )
        if key is None:
            return formattedCells

        for k, v in key.items():
            formattedCells = formattedCells.replace(str(k), str(v))

        return formattedCells

    @staticmethod
    def checkWin(player, cells):
        c = cells
        tr = c[0]  # Top Row
        mr = c[1]  # Middle Row
        br = c[2]  # Bottom Row
        lc = [c[i][0] for i in range(3)]  # Left Column
        mc = [c[i][1] for i in range(3)]  # Middle Column
        rc = [c[i][2] for i in range(3)]  # Right Column
        d1 = [c[i][i] for i in range(3)]  # Diagonal \
        d2 = [c[2 - i][i] for i in range(3)]  # Diagonal /

        for line in [tr, mr, br, lc, mc, rc, d1, d2]:
            if all(player == cell for cell in line):
                # Returns 1 or 2, which are truthy
                return player
        return False

    def hasWon(self):
        # May be useful when optimizing https://jayeshkawli.ghost.io/tic-tac-toe/
        if self.lastPos is None: return False  # If the game hasn't started, nobody has won
        y = self.lastPos[0]
        x = self.lastPos[1]
        lastPlayer = self.cells[y][x]

        self.win = self.checkWin(lastPlayer, self.cells)

        return self.win


if __name__ == '__main__':
    g = Grid()
    key = {0: ' ', 1: 'X', 2: 'O'}
    playerList = [None, RandomAIPlayer(1, delay=1), RandomAIPlayer(2, delay=1)]

    print(f"Initial Player is {playerList[g.currentPlayer].name} ({key[g.currentPlayer]})")

    try:
        while not g.hasWon() and g.movesLeft:
            player = playerList[g.currentPlayer]

            move = player.getMove(g.cells)
            print(f"{player.name}'s Turn ({key[g.currentPlayer]}): played {move}")

            try:
                g.play(player.playerNo, move)
            except AlreadyFilledError:
                print(f"move {move} is Invalid")
                continue

            print(g.getFormattedCells(key=key))

        if g.win:
            print(f"Game has ended in a win for {playerList[g.lastPlayer].name} ({key[g.currentPlayer]})")
        else:
            print("Game ended in a Draw!")

    except GridError as e:
        print(f"{e.__class__.__name__}: {e}")
        print(g.cells)
