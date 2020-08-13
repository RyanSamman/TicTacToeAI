import re


class Player:
    def __init__(self, playerNo, name=None):
        if name is None: name = f"Player #{playerNo}"
        self.name = name
        self.playerNo = playerNo

    def getMove(self, cells):
        while True:
            move = input("Your turn, make a move: ")
            if re.match(r"^[0-2][0-2]$", move):
                break
        return int(move[0]), int(move[1])

