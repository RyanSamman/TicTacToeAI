from tkinter import messagebox


class GridError(Exception):
    # Parent Error Class
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

if __name__ == '__main__':
    print("test")
