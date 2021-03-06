import time
from threading import BoundedSemaphore
from colors import *
from game_config import *

class Pheromone(object):
    def __init__(self, game, life_time=PHEROMONE_LIFE):
        self.matrix = [[0 for i in range(GAME_MATRIX_SIZE)] for i in range(GAME_MATRIX_SIZE)]
        self.matrix_sem = BoundedSemaphore()
        self.game = game
        self.life_time = life_time

    def get(self, position):
        with self.matrix_sem:
            return self.matrix[position[0]][position[1]]

    def add(self, position, life_time=None):
        accress_time = self.life_time if life_time is None else life_time
        with self.matrix_sem:
            if self.matrix[position[0]][position[1]]  < self.life_time * 5:
                self.matrix[position[0]][position[1]] += accress_time

    def update(self):
        for x in range(GAME_MATRIX_SIZE):
            for y in range(GAME_MATRIX_SIZE):
                with self.matrix_sem:
                    if self.matrix[x][y] == 0:
                        continue
                    else:
                        self.matrix[x][y] -= 1

                    if self.matrix[x][y] == 0:
                        self.game.clear_position(x, y)
                    else:
                        self.game.set_postion(CYAN, x, y)