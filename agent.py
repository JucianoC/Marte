import random
import time
from colors import *

class Agent(object):
    def __init__(self, position, game):
        self.position = position
        self.game = game

    def life(self):
        while not self.game.done:
            self.game.event.wait()
            self.move()

    def move(self):
        my_range = [
            value for value in 
            self.game.get_range(*self.position)
        ]
        if not my_range:
            return
        new_pos = random.choice(my_range)
        self.position = new_pos
        self.game.clear_position(*self.position)
        self.game.set_postion(WHITE, *self.position)