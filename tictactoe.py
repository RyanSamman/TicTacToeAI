import pygame
import thorpy
from os import path
from tkinter import messagebox, Tk, simpledialog
from threading import Thread
from multiprocessing import Process
from TicTacToe.Grid import Grid
from TicTacToe.util import saveData, displayData
from TicTacToe.Players.Player import Player
from TicTacToe.Players.AIPlayer import AIPlayer
from TicTacToe.Players.RandomAIPlayer import RandomAIPlayer
from TicTacToe.Exceptions.TicTacToeExceptions import AlreadyFilledError, WrongTurnError


class Game():
    def __init__(self, assetsPath, saveToCloud=True):
        self.grid = Grid()

        pygame.init()
        pygame.font.init()
        self.Font = pygame.font.SysFont('Calibri', 35)
        self.clock = pygame.time.Clock()
        self.assets = {}
        self.loadAssets(assetsPath)

        pygame.display.set_caption('Tic Tac Toe')
        pygame.display.set_icon(self.assets['icon'])

        self.WINDOW_WIDTH = 400
        self.WINDOW_HEIGHT = 450
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        self.setupUI()

        self.AIDelay = 1
        self.AIPlayer = AIPlayer(2, delay=self.AIDelay, name="Minimax AI")
        self.redraw()

        self.running = True

        while self.running:
            self.clock.tick(100)
            self.handleEvents()
            self.redraw()

            if self.grid.win or self.grid.movesLeft == 0:
                if self.grid.win and self.grid.lastPlayer == 1:
                    messagebox.showinfo(f'Win!', 'Congratulations, you won!')
                elif self.grid.win and self.grid.lastPlayer == 2:
                    messagebox.showinfo(f'Loss!', 'The AI has won!')
                else:
                    messagebox.showinfo(f'Draw!', 'The game has ended in a Draw!')

                if saveToCloud: self.saveGameData()
                self.selectAI()
                self.grid.restartGrid()
                self.redraw()

            if self.grid.currentPlayer == 2:
                move = self.AIPlayer.getMove(self.grid.cells)
                self.grid.play(2, move)
                self.redraw()

    def selectAI(self):
        try:
            AI = self.toggleButtonPool.get_selected().get_text()
            if AI == 'Random AI': self.AIPlayer = RandomAIPlayer(2, delay=0.5, name="Random AI")  # Set to Random AI
            else: self.AIPlayer = AIPlayer(2, delay=self.AIDelay, name="Minimax AI")  # Set to Minimax AI
        except AttributeError:
            self.AIPlayer = AIPlayer(2, delay=self.AIDelay, name="Minimax AI")  # Set to Minimax AI if any error occurs
        except Exception as e:
            messagebox.showerror(e.__class__.__name__, e)
            self.AIPlayer = AIPlayer(2, delay=self.AIDelay, name="Minimax AI")

    def setupUI(self):
        analyticsButton = thorpy.make_button('  Analytics  ', func=lambda: Process(target=displayData).start())
        analyticsButton.set_main_color((145, 195, 220))

        toggleButtons = [thorpy.Togglable('Minimax AI'), thorpy.Togglable('Random AI')]
        self.toggleButtonPool = thorpy.TogglablePool(toggleButtons, first_value=toggleButtons[0], always_value=True)

        self.box = thorpy.Box(elements=toggleButtons + [analyticsButton])
        self.box.set_main_color((255, 255, 255))

        self.menu = thorpy.Menu(self.box)

        for element in self.menu.get_population():
            element.surface = self.window

        self.box.blit()
        self.box.update()


    @staticmethod
    def cellPos(y, x):
        return (50 + x * 100), (130 + y * 100)

    def drawCells(self):
        key = [None, self.assets['X'], self.assets['O']]
        cells = self.grid.cells
        for y in range(3):
            for x in range(3):
                cell = cells[y][x]
                if cell == 0: continue
                self.window.blit(key[cell], (self.cellPos(y, x)))

    def saveGameData(self):
        playerList = [None, Player(1), self.AIPlayer]
        gameData = {
            'player1': playerList[1].__class__.__name__,
            'player2': playerList[2].__class__.__name__,
            'startingPlayer': playerList[self.grid.lastPlayer].__class__.__name__,
            'moves': 9 - self.grid.movesLeft,
            'win': True if self.grid.win else False,
            'winner': playerList[self.grid.lastPlayer].__class__.__name__ if self.grid.win else '',
            'draw': False if self.grid.win and self.grid.movesLeft != 9 else True
        }
        Thread(target=saveData, args=(gameData,)).start()

    def redraw(self):
        self.window.fill((255, 255, 255))
        pygame.draw.rect(self.window, (255, 255, 255), (50, 75, 300, 300))
        self.window.blit(self.assets['VLine'], (50 - 5 + 100, 125))
        self.window.blit(self.assets['VLine'], (50 - 5 + 200, 125))
        self.window.blit(self.assets['HLine'], (50, 125 + 100))
        self.window.blit(self.assets['HLine'], (50, 125 + 200))
        self.drawCells()
        self.box.blit()
        self.box.update()
        self.displayTurn()
        pygame.display.update()

    def displayTurn(self):
        playerName = "Your" if self.grid.currentPlayer == 1 else f"{self.AIPlayer.name}'s"
        currentTurnText = self.Font.render(f"{playerName} turn", True, (0, 0, 0))
        rect = currentTurnText.get_rect(center=(self.WINDOW_WIDTH // 2, 60))
        self.window.blit(currentTurnText, rect)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN: self.handleClick(pygame.mouse.get_pos())
            self.menu.react(event)

    def handleClick(self, mousePos):
        x, y = mousePos
        if 350 >= x >= 50 and 425 >= y >= 125:
            move = ((y - 125) // 100, (x - 50) // 100)
            try:
                self.grid.play(1, move)
            except WrongTurnError:
                messagebox.showerror('Error', 'Wait for your turn')
            except AlreadyFilledError:
                messagebox.showerror('Error', 'Position already filled')
            self.redraw()

    def loadAssets(self, assetsPath):
        self.assets['VLine'] = pygame.image.load(path.join(*assetsPath, 'line.png'))
        self.assets['HLine'] = pygame.transform.rotate(self.assets['VLine'], 90)
        self.assets['X'] = pygame.image.load(path.join(*assetsPath, 'X.png'))
        self.assets['O'] = pygame.image.load(path.join(*assetsPath, 'O.png'))
        self.assets['icon'] = pygame.image.load(path.join(*assetsPath, 'icon.png'))


if __name__ == '__main__':
    # For the messagebox, to prevent a Tkinter window from popping up
    root = Tk()
    root.withdraw()
    try:
        Game(assetsPath=('TicTacToe', 'Resources'), saveToCloud=True)
    except Exception as e:
        messagebox.showerror('ERROR', f'{e.__class__.__name__}: {e}')
        raise e
