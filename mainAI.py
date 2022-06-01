import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
import math

pygame.init()
font = pygame.font.Font("IBM.ttf", 25)


# TODO: reset method, reward method, play method that gives direction, game iteration

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple("Point", "x, y")

BLOCK_SIZE = 20
SPEED = 50

BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
TURQUOISE = (0, 255, 255)
WHITE = (255, 255, 255)
PINK = (255, 51, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (127, 0, 255)





class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        self.reset()

    def reset(self):
        # initial direction
        self.direction = Direction.RIGHT

        self.color = rando_col()

        # start head position
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        self.last_head = Point(None, None)

    def _place_food(self):
        while True:

            x = random.randint(1, 31) * 20
            y = random.randint(1, 23) * 20

            self.food = Point(x, y)

            if not self.inside_snake(self.food):
                break

        # check if this creates issues may have to change to self.head rather than snake NEVERMIND

    def play_step(self, action):

        self.frame_iteration += 1

        self._move(action)
        self.snake.insert(0, self.head)

        reward = 0

        game_over = False
        if self.is_collision():
            game_over = True
            reward = -30
            self.last_head = self.head
            return reward, game_over, self.score

        elif self.is_collision_bod():
            game_over = True
            reward = -50
            self.last_head = self.head
            return reward, game_over, self.score

        elif self.frame_iteration > 60 * len(self.snake):
            game_over = True
            reward = -200
            self.last_head = self.head
            return reward, game_over, self.score

        # compares value of current head to last head to determine if snake is moving in the direction of the food and
        # rewards it accordingly
        if self.distance(self.head) < self.distance(self.last_head) and self.last_head.x is not None:
            reward = ((640 - self.distance(self.head)) // (self.score + 1 * 0.5)) * 0.01

        # Checks if food is eaten by snake
        if self.head == self.food and self.head != self.snake[1:]:
            self.score += 1
            # FIXME: possible issue here may need to be changed to +=
            reward = 10 * (self.score + 1)
            self._place_food()
            self.last_head = self.head
        # If food is not eaten by snake pop the part of the snake.
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(SPEED)
        self.last_head = self.head
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head

        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        return False

        # FIXME: possible issue here as I added a new parameter "pt" which may interfere with this loop
        # checks if the head intersects with a part of the snake

    def is_collision_bod(self, pt=None):
        if pt is None:
            pt = self.head

        pt_counter = 0
        for i in self.snake:
            if pt_counter != 0:
                if pt.x == i.x and pt.y == i.y:
                    return True
            pt_counter += 1

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, self.color, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, self.color, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]

        self.direction = new_dir
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

    def inside_snake(self, pt):
        pt_counter = 0
        for i in self.snake:
            if pt_counter != 0:
                if pt.x == i.x and pt.y == i.y:
                    return True
            pt_counter += 1

    def distance(self, pt):
        if pt.x is None or pt.y is None:
            return 200
        x = abs(pt.x - self.food.x)
        y = abs(pt.y - self.food.y)
        d = math.sqrt(x ** 2 + y ** 2)
        # print(d, pt, self.food)
        return d


def rando_col():
    col_arr = [BLUE1, WHITE, PINK, TURQUOISE, YELLOW, GREEN, PURPLE]
    rand_idx = random.randint(0, len(col_arr)-1)
    return col_arr[rand_idx]
