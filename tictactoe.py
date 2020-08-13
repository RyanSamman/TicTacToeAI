import pygame
from os import path


class Game:
    def __init__(self, *assetPath):
        self.clock = pygame.time.Clock()
        self.running = True

        self.assets = {}
        self.loadAssets(*assetPath)

        self.WINDOW_WIDTH = 400
        self.WINDOW_HEIGHT = 400
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        pygame.init()

        while self.running:
            self.clock.tick(100)
            self.handleEvents()
            self.redraw()

    def redraw(self):
        pygame.draw.rect(self.window, (255, 255, 255), (50, 75, 300, 300))
        self.window.blit(self.assets['VLine'], (50 - 5 + 100, 75))
        self.window.blit(self.assets['VLine'], (50 - 5 + 200, 75))
        self.window.blit(self.assets['HLine'], (50, 75 + 100))
        self.window.blit(self.assets['HLine'], (50, 75 + 200))
        self.window.blit(self.assets['O'], (50, 80))
        self.window.blit(self.assets['O'], (50 + 1 * 100, 80 + 1 * 100))
        self.window.blit(self.assets['X'], (50 + 1 * 100, 80 + 2 * 100))
        pygame.display.update()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False

    def loadAssets(self, *assetsPath):

        self.assets['VLine'] = pygame.image.load(path.join(*assetsPath, 'line.png'))
        self.assets['HLine'] = pygame.transform.rotate(self.assets['VLine'], 90)
        self.assets['X'] = pygame.image.load(path.join(*assetsPath, 'X.png'))
        self.assets['O'] = pygame.image.load(path.join(*assetsPath, 'O.png'))


if __name__ == '__main__':
    Game('Resources')
