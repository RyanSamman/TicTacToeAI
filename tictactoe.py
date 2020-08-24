import pygame
import thorpy
from os import path
from threading import Thread
from tkinter import messagebox, Tk
from multiprocessing import Process

from TicTacToe import Grid
from TicTacToe import GameException
from TicTacToe import TicTacToeExceptions
from TicTacToe.util import saveData, displayData
from TicTacToe import Player, AIPlayer, RandomAIPlayer


class Game():
    def __init__(self, assetsPath, saveToCloud=True):
        # For the messagebox, to prevent a Tkinter window from popping up
        root = Tk()
        root.withdraw()

        self.grid = Grid()
        self.AI_DELAY = 1
        self.selectAI()

        self.COLOR = {
            'BLACK': (000, 000, 000),
            'BLUE':  (145, 195, 220),
            'WHITE': (255, 255, 255)
        }

        self.LINE_WIDTH = 10
        self.HEADER_HEIGHT = 125
        self.SIDE_PADDING = 50
        self.GRID_SIZE = 300
        self.H_CELLS = 3 # Horizontal Cells in the Grid
        self.TOTAL_MOVES = self.H_CELLS * 3
        self.CELL_WIDTH = self.GRID_SIZE // self.H_CELLS
        
        self.WINDOW_WIDTH = self.SIDE_PADDING + self.GRID_SIZE + self.SIDE_PADDING
        self.WINDOW_HEIGHT = self.HEADER_HEIGHT + self.GRID_SIZE + 25 # Pad the bottom with 25px

        self.assets = {}
        self.loadAssets(assetsPath)

        pygame.init()
        pygame.font.init()
        self.Font = pygame.font.SysFont('Calibri', 30)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('Tic Tac Toe')
        pygame.display.set_icon(self.assets['icon'])

        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        self.setupUI()
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
            if AI == 'Random AI': self.AIPlayer = RandomAIPlayer(2, delay=self.AI_DELAY, name="Random AI")  # Set to Random AI
            else: self.AIPlayer = AIPlayer(2, delay=self.AI_DELAY, name="Minimax AI")  # Set to Minimax AI
        except AttributeError:
            self.AIPlayer = AIPlayer(2, delay=self.AI_DELAY, name="Minimax AI")  # Set to Minimax AI if any error occurs
        except Exception as e:
            messagebox.showerror(e.__class__.__name__, e)
            self.AIPlayer = AIPlayer(2, delay=self.AI_DELAY, name="Minimax AI")

    def setupUI(self):
        BUTTON_SIZE = (80, 28) # Default Button Size, 120px wide and 30px high

        analyticsButton = thorpy.make_button('Analytics', func=lambda: Process(target=displayData).start())
        analyticsButton.set_main_color(self.COLOR['BLUE'])
        analyticsButton.set_size(BUTTON_SIZE)

        toggleButtons = [thorpy.Togglable('Minimax AI'), thorpy.Togglable('Random AI')]
        self.toggleButtonPool = thorpy.TogglablePool(toggleButtons, first_value=toggleButtons[0], always_value=True)

        self.box = thorpy.Box(elements=toggleButtons + [analyticsButton])
        self.box.set_main_color(self.COLOR['WHITE'])

        self.menu = thorpy.Menu(self.box)

        for element in self.menu.get_population():
            element.surface = self.window

        self.box.blit()
        self.box.update()


    def cellPos(self, y, x):
        return (self.SIDE_PADDING + x * self.CELL_WIDTH), (self.HEADER_HEIGHT + self.LINE_WIDTH // 2 + y * self.CELL_WIDTH)

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
            'moves': self.TOTAL_MOVES - self.grid.movesLeft,
            'win': True if self.grid.win else False,
            'winner': playerList[self.grid.lastPlayer].__class__.__name__ if self.grid.win else '',
            'draw': False if self.grid.win and self.grid.movesLeft != self.TOTAL_MOVES else True
        }
        Thread(target=saveData, args=(gameData,)).start()

    def redraw(self):
        self.window.fill((255, 255, 255))
        pygame.draw.rect(self.window, self.COLOR['WHITE'], (self.SIDE_PADDING, self.HEADER_HEIGHT, self.GRID_SIZE, self.GRID_SIZE))
        self.window.blit(self.assets['VLine'], (self.SIDE_PADDING - (self.LINE_WIDTH // 2) + self.CELL_WIDTH, self.HEADER_HEIGHT))
        self.window.blit(self.assets['VLine'], (self.SIDE_PADDING - (self.LINE_WIDTH // 2) + 2 * self.CELL_WIDTH, self.HEADER_HEIGHT))
        self.window.blit(self.assets['HLine'], (self.SIDE_PADDING, self.HEADER_HEIGHT + self.CELL_WIDTH))
        self.window.blit(self.assets['HLine'], (self.SIDE_PADDING, self.HEADER_HEIGHT + 2 * self.CELL_WIDTH))
        self.drawCells()
        self.box.blit()
        self.box.update()
        self.displayTurn()
        pygame.display.update()

    def displayTurn(self):
        playerName = "Your" if self.grid.currentPlayer == 1 else f"{self.AIPlayer.name}'s"
        currentTurnText = self.Font.render(f"{playerName} turn", True, self.COLOR['BLACK'])
        rect = currentTurnText.get_rect(center=(self.WINDOW_WIDTH // 2, self.HEADER_HEIGHT // 2))
        self.window.blit(currentTurnText, rect)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.running = False
        
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                mousePosition = pygame.mouse.get_pos()
                self.handleClick(mousePosition)
            self.menu.react(event)

    def handleClick(self, mousePos):
        x, y = mousePos
        if self.GRID_SIZE + self.SIDE_PADDING >= x >= self.SIDE_PADDING and self.HEADER_HEIGHT + self.GRID_SIZE >= y >= self.HEADER_HEIGHT:
            move = ((y - self.HEADER_HEIGHT) // self.LINE_WIDTH, (x - self.SIDE_PADDING) // self.LINE_WIDTH)
            try:
                self.grid.play(1, move)
            except TicTacToeExceptions.WrongTurnError:
                messagebox.showerror('Error', 'Wait for your turn')
            except TicTacToeExceptions.AlreadyFilledError:
                messagebox.showerror('Error', 'Position already filled')
            self.redraw()

    def loadAssets(self, assetsPath):
        self.assets['VLine'] = pygame.image.load(path.join(*assetsPath, 'line.png'))
        self.assets['HLine'] = pygame.transform.rotate(self.assets['VLine'], 90) # Rotate 90 degrees

        self.assets['X'] = pygame.image.load(path.join(*assetsPath, 'X.png'))
        self.assets['O'] = pygame.image.load(path.join(*assetsPath, 'O.png'))

        self.assets['icon'] = pygame.image.load(path.join(*assetsPath, 'icon.png'))


if __name__ == '__main__':
    try:
        Game(assetsPath=('TicTacToe', 'Resources'), saveToCloud=True)
    except GameException as e:
        messagebox.showerror('ERROR', f'{e.__class__.__name__}: {e}')
        raise e
