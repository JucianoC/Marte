import pygame
import random
from threading import Thread, Event, BoundedSemaphore
from colors import *
from agent import Agent
from pheromone import Pheromone

BACKGROUND = MARTE
GAME_MATRIX_SIZE = 25
AGENT_NUMBER = 1

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

        for i in range(int(0.1*GAME_MATRIX_SIZE*GAME_MATRIX_SIZE)):
            pos_gema = (random.randint(0, GAME_MATRIX_SIZE-1), random.randint(0, GAME_MATRIX_SIZE-1))
            pos_rock = (random.randint(0, GAME_MATRIX_SIZE-1), random.randint(0, GAME_MATRIX_SIZE-1))
            
            if self.game_map[pos_gema[0]][pos_gema[1]] is None:
                gem = random.choice(GEMS)
                self.game_map[pos_gema[0]][pos_gema[1]] = gem
            
            if self.game_map[pos_rock[0]][pos_rock[1]] is None:
                self.game_map[pos_rock[0]][pos_rock[1]] = ROCK

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
            for y in range(-2, 3):
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
        self.pheromone_controller.start()

    def update(self):
        with self.map_sem:
            self.screen.fill(BACKGROUND)
            for x in range(GAME_MATRIX_SIZE):
                for y in range(GAME_MATRIX_SIZE):
                    if not self.game_map[x][y] is None:
                        pygame.draw.rect(game.screen, self.game_map[x][y], [x*16, y*16, 16, 16])
            pygame.display.flip()

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

    for agent in game.agents:
        t = Thread(target=agent.life)
        t.start()

    while not game.done:
        game.event.clear()
        clock.tick(7)       
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                game.done = True

            game.update()
        game.event.set()