import pygame
import random
from colors import *

BACKGROUND = MARTE
GAME_MATRIX_SIZE = 25

class Game(object):

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Marte")
        self.screen = pygame.display.set_mode((16*GAME_MATRIX_SIZE, 16*GAME_MATRIX_SIZE))
        self.screen.fill(BACKGROUND)
        self.done = False
        self.mothership_position = (random.randint(0, GAME_MATRIX_SIZE-1), random.randint(0, GAME_MATRIX_SIZE-1))
        self.game_map = [[None for i in range(GAME_MATRIX_SIZE)] for i in range(GAME_MATRIX_SIZE)]

        self.game_map[self.mothership_position[0]][self.mothership_position[1]] = WHITE

        for i in range(int(0.1*GAME_MATRIX_SIZE*GAME_MATRIX_SIZE)):
            pos_gema = (random.randint(0, GAME_MATRIX_SIZE-1), random.randint(0, GAME_MATRIX_SIZE-1))
            pos_rock = (random.randint(0, GAME_MATRIX_SIZE-1), random.randint(0, GAME_MATRIX_SIZE-1))
            
            if self.game_map[pos_gema[0]][pos_gema[1]] is None:
                gem = random.choice(GEMS)
                self.game_map[pos_gema[0]][pos_gema[1]] = gem
            
            if self.game_map[pos_rock[0]][pos_rock[1]] is None:
                self.game_map[pos_rock[0]][pos_rock[1]] = ROCK


    def clear_position(self, x, y):
        self.game_map[x][y] = None

    def set_postion(self, color, x, y):
        self.game_map[x][y] = color        

    def refresh(self):
        self.screen.fill(BACKGROUND)
        for x in range(GAME_MATRIX_SIZE):
            for y in range(GAME_MATRIX_SIZE):
                if not self.game_map[x][y] == None:
                    pygame.draw.rect(self.screen, self.game_map[x][y], [x*16, y*16, 16, 16])
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    clock = pygame.time.Clock()

    while not game.done: 
        clock.tick(10)     
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                game.done = True

        game.refresh()