class AIError(Exception):
    # Base AI Error Class
    pass


class InvalidCellsError(AIError):
    def __init__(self):
        super().__init__(f"The AI cannot process a grid that isn't 3x3")


class NoPossibleMovesError(AIError):
    def __init__(self):
        super().__init__(f"The AI could not find any valid moves")
