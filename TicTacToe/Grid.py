from TicTacToe.Exceptions import GridError, InvalidGridIndexError, AlreadyFilledError, WrongTurnError, GameEndedError
from random import randint


class Grid:
    def __init__(self):
        self.restart()

    def restart(self, startingPlayer=randint(1, 2)):
        self.cells = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.currentPlayer = startingPlayer
        self.win = False
        self.movesLeft = 9
        self.lastPos = None

    def play(self, player, move):
        print(f"It's Player {self.currentPlayer}'s turn")
        print(f'Player {player} selected {i1, i2}')
        if self.currentPlayer != player: raise WrongTurnError(self.currentPlayer)
        self.setCell(y=move[0], x=move[1])
        self.movesLeft -= 1
        self.lastPos = move
        self.lastPlayer = player
        self.switchToNextPlayer()
        print(self.getFormattedCells())

        return self.cells

    def setCell(self, y, x):
        if self.win or not self.movesLeft: raise GameEndedError()
        if not (3 > x >= 0 and 3 > y >= 0): raise InvalidGridIndexError(x, y)
        if self.cells[y][x]: raise AlreadyFilledError(x, y)
        self.cells[y][x] = self.currentPlayer

    def switchToNextPlayer(self):
        self.currentPlayer = 2 if self.currentPlayer == 1 else 1
        return self.currentPlayer

    def getFormattedCells(self):
        f = self.cells
        return (
            f"{f[0][0]}|{f[0][1]}|{f[0][2]}\n"
            f"{f[1][0]}|{f[1][1]}|{f[1][2]}\n"
            f"{f[2][0]}|{f[2][1]}|{f[2][2]}\n"
        )

    def hasWon(self):
        # May be useful when optimizing https://jayeshkawli.ghost.io/tic-tac-toe/
        if self.win: return True  # Won if already won and haven't reset
        if self.lastPos is None: return False  # If the game hasn't started, nobody has won
        y = self.lastPos[0]
        x = self.lastPos[1]
        lastPlayer = self.cells[y][x]

        self.win = False

        c = self.cells

        tr = c[0]  # Top Row
        mr = c[1]  # Middle Row
        br = c[2]  # Bottom Row
        lc = [c[i][0] for i in range(3)]  # Left Column
        mc = [c[i][1] for i in range(3)]  # Middle Column
        rc = [c[i][2] for i in range(3)]  # Right Column
        d1 = [c[i][i] for i in range(3)]  # Diagonal \
        d2 = [c[2 - i][i] for i in range(3)]  # Diagonal /

        for line in [tr, mr, br, lc, mc, rc, d1, d2]:
            if all(lastPlayer == cell for cell in line):
                self.win = True
                break

        return self.win


if __name__ == '__main__':
    g = Grid()
    p1Moves = [(0, 2), (1, 2), (2, 2), (2, 1), (1, 1)]
    p2Moves = [(2, 0), (1, 0), (0, 0), (0, 1), (1, 1)]
    player = g.currentPlayer
    print(f"Initial Player is Player {player}")

    try:
        i1 = i2 = win = 0
        while not g.hasWon() and g.movesLeft:
            if player == 1:
                g.play(player, p1Moves[i1])
                i1 += 1
            elif player == 2:
                g.play(player, p2Moves[i2])
                i2 += 1

            player = g.currentPlayer

        if g.win:
            print("Game has ended in a win for Player", g.lastPlayer)
        else:
            print("Draw")

    except GridError as e:
        print(f"{e.__class__.__name__}: {e}")
        print(g.cells)
