import time
from threading import BoundedSemaphore, Thread
from colors import *
from game import GAME_MATRIX_SIZE

class Pheromone(object):
    def __init__(self, game, life_time=10):
        self.matrix = [[0 for i in range(GAME_MATRIX_SIZE)] for i in range(GAME_MATRIX_SIZE)]
        self.matrix_sem = BoundedSemaphore()
        self.game = game
        self.life_time = life_time

    def add(self, position):
        with self.matrix_sem:
            self.matrix[position[0]][position[1]] += self.life_time

    def update(self):
        for x in range(GAME_MATRIX_SIZE):
            for y in range(GAME_MATRIX_SIZE):
                with self.matrix_sem:
                    if self.matrix[x][y] == 0:
                        continue
                    else:
                        self.matrix[x][y] -= 1

                    if not self.game.game_map[x][y] in AGENT_COLORS:
                        if self.matrix[x][y] == 0:
                            self.game.clear_position(x, y)
                        else
                            self.game.set_postion(CYAN, x, y)

    def loop(self):
        while True:
            time.sleep(1)
            self.update()

    def start(self):
        Thread(target=loop).start()