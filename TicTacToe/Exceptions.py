from tkinter import messagebox


class GridError(Exception):
    # Base TicTacToe Grid Error Class
    pass


class InvalidGridIndexError(GridError):
    def __init__(self, x, y):
        super().__init__(f'Position ({x}, {y}) is not on the Board!')
    pass


class AlreadyFilledError(GridError):
    def __init__(self, x, y):
        super().__init__(f'Position ({x}, {y}) is already filled!')
    pass


class WrongTurnError(GridError):
    def __init__(self, currentPlayer):
        super().__init__(f"It is Player {currentPlayer}'s turn")


class GameEndedError(GridError):
    def __init__(self):
        super().__init__(f"The Game has ended")


class AIError(Exception):
    # Base AI Error Class
    pass


class InvalidCellsError(AIError):
    def __init__(self):
        super().__init__(f"The AI cannot process a grid that isn't 3x3")


class NoPossibleMovesError(AIError):
    def __init__(self):
        super().__init__(f"The AI could not find any valid moves")


if __name__ == '__main__':
    print("test")
