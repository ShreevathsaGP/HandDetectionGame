# game.py

import sys
import math
import pygame
import random
import pygame
from globy import *

class Breakout:
    # brick
    no_brick_rows = 5
    brick_height = 45
    brick_width_range = (75, 150)
    brick_space = 7 # space between bricks

    # layout
    x_space = 20
    y_space = 80
    x_bounds = [x_space, window_width - x_space]
    brick_bottom = (no_brick_rows * brick_height) + (no_brick_rows * brick_space) + y_space

    # paddle
    paddle_width = 200
    paddle_height = 20
    y_bottom = 15

    # ball
    ball_radius = 27

    def __init__(self):
        # instance variables
        self.bricks = []
        self.paddle = pygame.Rect(window_width/2 - self.paddle_width/2, 
                window_height - self.y_bottom - self.paddle_height, 
                self.paddle_width, 
                self.paddle_height)
        self.ball = Vector(window_width // 2, self.brick_bottom + self.ball_radius)
        self.ball_velocity = Vector(6, 6)
        self.score = 0

        # create random bricks [ within width range ]
        for r in range(self.no_brick_rows):
            x = self.x_space
            y = self.y_space + (r * (self.brick_space + self.brick_height))
            iterate = True
            while iterate:
                width = random.randrange(*self.brick_width_range)
                if x + width > (window_width - self.x_space):
                    width = (window_width - self.x_space - x)
                    self.bricks.append(pygame.Rect(x, y, width, self.brick_height))
                    iterate = False
                elif (window_width - self.x_space) - (x + width + self.x_space) <= self.x_space:
                    width += ((window_width - self.x_space) - (x + width + self.x_space))
                    self.bricks.append(pygame.Rect(x, y, width, self.brick_height))
                else:
                    self.bricks.append(pygame.Rect(x, y, width, self.brick_height))
                    x += (width + self.brick_space)
        self.brick_render = [True] * len(self.bricks)

    def update_paddle(self, x):
        self.paddle.x = x

    def x_in_bounds(self, x):
        return (self.x_bounds[0] <= x <= (self.x_bounds[1] - self.paddle_width))

    def render_brick(self, index):
        return self.brick_render[index]

    def check_collisions(self):
        # ball velocity components
        vel_x = self.ball_velocity.x
        vel_y = self.ball_velocity.y
        
        # impact point [ y ]
        if vel_y > 0:
            x = self.ball.x
            y = self.ball.y + self.ball_radius
        elif vel_y < 0:
            x = self.ball.x
            y = self.ball.y - self.ball_radius
        else:
            y = self.ball.y

        # impact point [ x ]
        if vel_x < 0:
            x = self.ball.x - self.ball_radius
        elif vel_x > 0:
            x = self.ball.x + self.ball_radius
        else:
            x = self.ball.x

        # wall collision
        if x >= window_width or x <= 0:
           self.ball_velocity.x *= -1
        if y >= window_height or y <= 0:
            self.ball_velocity.y *= -1

        # if within y bounds of bricks
        if (self.y_space - self.ball_radius) <= self.ball.y <= (self.brick_bottom + self.ball_radius):
            # brick collision [ all edges ]
            for index, brick in enumerate(self.bricks):
                if brick:
                    # top
                    if (brick.x <= self.ball.x <= brick.x + brick.w) and (brick.y <= self.ball.y - self.ball_radius <= brick.y + brick.h):
                        self.brick_render[index] = False
                        self.ball_velocity.y *= -1
                        break

                    # bottom
                    if (brick.x <= self.ball.x <= brick.x + brick.w) and (brick.y <= self.ball.y + self.ball_radius <= brick.y + brick.h):
                        self.brick_render[index] = False
                        self.ball_velocity.y *= -1
                        break
            
            for index, brick in enumerate(self.brick_render):
                if not brick: self.bricks[index] = None

        # paddle collision
        paddle_sections = self.paddle_width / 3
        if (self.paddle.x <= x <= self.paddle.x + self.paddle.w) and (self.paddle.y <= y <= self.paddle.y + self.paddle.h):
            # if self.x
            self.ball_velocity.y *= -1
            return
        if (self.paddle.x <= x - self.ball_radius <= self.paddle.x + self.paddle.w) and (self.paddle.y <= y <= self.paddle.y + self.paddle.h):
            self.ball_velocity.y *= -1
            return
        if (self.paddle.x <= x + self.ball_radius <= self.paddle.x + self.paddle.w) and (self.paddle.y <= y <= self.paddle.y + self.paddle.h):
            self.ball_velocity.y *= -1
            return

    def update(self):
        # ball bounces
        self.ball += self.ball_velocity

    def get_objects(self):
        return (self.paddle, self.bricks, self.ball)



