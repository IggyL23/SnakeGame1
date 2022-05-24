import pygame
import random
from enum import Enum
from collections import namedtuple


pygame.init()
font = pygame.font.Font("IBM.ttf", 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple("Point", "x, y")

BLOCK_SIZE = 20
SPEED = 40

BLACK = (0,0,0)
RED = (200,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
WHITE = (255,355,255)




class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, Point(self.head.x-BLOCK_SIZE, self.head.y),Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, ((self.w-BLOCK_SIZE)//int(BLOCK_SIZE))*BLOCK_SIZE)
        y = random.randint(0, ((self.w - BLOCK_SIZE) //int(BLOCK_SIZE)) * BLOCK_SIZE)
        self.food = Point(x,y)

        # check if this creates issues may have to change to self.head rather than snake NEVERMIND
        if self.food in self.snake:
            self._place_food()


    def play_step(self):

        self._update_ui()
        self.clock.tick(SPEED)

        game_over = False
        return game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw(self.display, BLUE1, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))




if __name__ == '__main__':
    game = SnakeGame()

    while True:
       game_over, score = game.play_step()
       if game_over == True:
            break

    print("Final Score", score)



    pygame.quit()
