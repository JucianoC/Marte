import pygame
import random
from threading import Thread, Event, BoundedSemaphore
from colors import *
from game_config import *

from agent import Agent
from pheromone import Pheromone

class Game(object):

    def __init__(self, clock):
        pygame.init()
        pygame.display.set_caption("Marte")
        self.screen = pygame.display.set_mode((16*GAME_MATRIX_SIZE, 16*GAME_MATRIX_SIZE))
        self.screen.fill(BACKGROUND)
        self.clock = clock
        self.done = False
        self.agents = []
        self.event = Event()
        self.pheromone_controller = None

        self.mothership_position = (random.randint(0, GAME_MATRIX_SIZE-1), random.randint(0, GAME_MATRIX_SIZE-1))
        self.game_map = [[None for i in range(GAME_MATRIX_SIZE)] for i in range(GAME_MATRIX_SIZE)]
        self.map_sem = BoundedSemaphore()

        self.game_map[self.mothership_position[0]][self.mothership_position[1]] = MAGENTA

        for i in range(int(FILL_MATRIX_ROCKS*GAME_MATRIX_SIZE*GAME_MATRIX_SIZE)):
            pos_rock = (random.randint(0, GAME_MATRIX_SIZE-1), random.randint(0, GAME_MATRIX_SIZE-1))
            
            if self.game_map[pos_rock[0]][pos_rock[1]] is None:
                self.game_map[pos_rock[0]][pos_rock[1]] = ROCK

        empty_slots = set()
        for x in range(GAME_MATRIX_SIZE):
            for y in range(GAME_MATRIX_SIZE):
                if self.game_map[x][y] is None:
                    empty_slots.add((x, y))

        for i in range(GEM_CENTERS):
            gem_center = random.choice(list(empty_slots))
            gem_range = [
                value for value in 
                Game.get_range(gem_center[0], gem_center[1], distance=GEM_RANGE, tower_mode=False)
                if self.game_map[value[0]][value[1]] is None
            ]
            for j in range(int(len(gem_range) * GEM_FILL)):
                if not empty_slots: break
                gem_position = random.choice(gem_range)
                empty_slots.remove(gem_position)
                gem_range.remove(gem_position)
                self.game_map[gem_position[0]][gem_position[1]] = random.choice(GEMS)

        mship_range = [
            value for value in 
            Game.get_range(
                self.mothership_position[0],
                self.mothership_position[1],
                distance=AGENT_NUMBER, tower_mode=False
            ) if not value is None
        ]

        for i in range(AGENT_NUMBER):
            if mship_range:
                pos = random.choice(mship_range)
                self.game_map[pos[0]][pos[1]] = WHITE
                mship_range.remove(pos)

    @classmethod
    def get_range(self, base_x, base_y, distance=1, tower_mode=True):
        map_range = []
        for x in range(-distance, distance+1):
            for y in range(-distance, distance+1):
                if x == 0 and y == 0: 
                    continue
                if tower_mode and (x != 0 and y != 0):
                    continue
                pos_x = base_x + x
                pos_y = base_y + y
                if pos_x >= GAME_MATRIX_SIZE or pos_x < 0:
                    continue
                if pos_y >= GAME_MATRIX_SIZE or pos_y < 0:
                    continue
                map_range.append((pos_x, pos_y))
        return map_range

    def create_agents(self):
        for x in range(GAME_MATRIX_SIZE):
            for y in range(GAME_MATRIX_SIZE):
                if self.game_map[x][y] == WHITE:
                    self.agents.append(Agent((x, y), self))

    def start_pheromone_controller(self):
        self.pheromone_controller = Pheromone(self)

    def clear_position(self, x, y):
        with self.map_sem:
            self.game_map[x][y] = None

    def set_postion(self, color, x, y):
        with self.map_sem:
            self.game_map[x][y] = color        


if __name__ == "__main__":
    clock = pygame.time.Clock()
    game = Game(clock)
    game.create_agents()
    game.start_pheromone_controller()

    for agent in game.agents:
        t = Thread(target=agent.life)
        t.start()

    while not game.done:
        game.event.clear()
        clock.tick(SPEED)       
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                game.done = True

        with game.map_sem:
            game.screen.fill(BACKGROUND)
            for x in range(GAME_MATRIX_SIZE):
                for y in range(GAME_MATRIX_SIZE):
                    if not game.game_map[x][y] is None:
                        pygame.draw.rect(game.screen, game.game_map[x][y], [x*16, y*16, 16, 16])
        game.pheromone_controller.update()
        pygame.display.flip()
        game.event.set()