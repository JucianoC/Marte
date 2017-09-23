import time
from threading import Thread
from colors import *

class Pheromone(object):
    def __init__(self, position, game, life_time=10):
        self.position = position
        self.game = game
        self.life_time = life_time

    def life(self):
        self.game.set_postion(CYAN, *self.position)
        time_index = 0.0
        while time_index < self.life_time:
            if self.game.done:
                return
            if not self.game.game_map[self.position[0]][self.position[1]] in AGENT_COLORS:
                self.game.set_postion(CYAN, *self.position)
            time.sleep(1)
            time_index += 1
        if not self.game.game_map[self.position[0]][self.position[1]] in AGENT_COLORS:
            self.game.clear_position(*self.position)

    def start(self):
        t = Thread(target=self.life)
        t.start()