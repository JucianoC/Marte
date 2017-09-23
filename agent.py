import random
import time
from colors import *

class Agent(object):

    def __init__(self, position, game):
        self.position = position
        self.game = game
        self.full = False
        self.color = WHITE
        self.chaos_chance = 0.01

    def togle_status(self):
        self.full = not self.full
        self.color = WHITE if not self.full else METAL

    def life(self):
        while not self.game.done:
            self.game.event.wait()
            self.move()

    def move(self):
        my_range = [
            value for value in 
            self.game.get_range(*self.position)
            if self.game.game_map[value[0]][value[1]] != ROCK
        ]
        if not my_range:
            raise Exception("Robot traped!")

        if not self.full:
            self.gem_search(my_range)
        else:
            self.mship_search(my_range)

    def move_to(self, destine):
        self.game.clear_position(*self.position)
        self.position = destine
        self.game.set_postion(self.color, *self.position)

    def move_to_empty(self, my_range, target=None):
        empty_range = [
            value for value in my_range 
            if self.game.game_map[value[0]][value[1]] is None
        ]
        if not empty_range:
            raise Exception("Robot traped!")
        
        if target is None:
            self.move_to(random.choice(empty_range))
        else:
            chaos = random.random()
            if chaos <= self.chaos_chance:
                self.move_to_empty(my_range)
            else:
                self.move_to(
                    empty_range[self.get_min_dist_index(
                        empty_range, target
                    )]
                )

    def gem_search(self, my_range):
        gem_range = [
            value for value in my_range 
            if self.game.game_map[value[0]][value[1]] in GEMS
        ]
        if gem_range:            
            self.move_to(random.choice(gem_range))
            self.togle_status()        
        else:
            self.move_to_empty(my_range)

    def mship_search(self, my_range):
        mship_range = [
            value for value in my_range 
            if self.game.game_map[value[0]][value[1]] == MAGENTA
        ]
        if mship_range:
            self.togle_status()        
        else:
            self.move_to_empty(my_range, self.game.mothership_position)

    def distance(self, a, b):
        return (((b[0] - a[0])**2)+((b[1] - a[1])**2))**0.5

    def get_min_dist_index(self, avaliable_list, target):
        dist_list = [
            self.distance(value, target) for value in avaliable_list
        ]
        return dist_list.index(min(dist_list))