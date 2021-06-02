# environment.py

import sys
import math
import pygame
import random
import pygame
import pymunk
import pymunk.pygame_util
from globy import *

# rules
pymunk.pygame_util.positive_y_is_up = True

# envionnment
class Environment:
    def __init__(self):
        # dimensions
        self.size = (window_width, window_height)
        self.space = pymunk.Space()
        self.space.gravity = 0, -900

        # bounding box
        box_space = 5
        self.vertices = [(box_space, box_space), (window_width - box_space, box_space),
                (window_width - box_space, window_height - box_space),
                (box_space, window_height - box_space)]
        for i in range(len(self.vertices)):
            segment = pymunk.Segment(self.space.static_body, self.vertices[i], self.vertices[(i+1) % len(self.vertices)], 2)
            segment.elasticity = 1 # all energy = kinetic energy
            self.space.add(segment)

        # particles
        self.no_particles = 5
        for _ in range(self.no_particles):
            impulse = (random.randrange(-100, 101), random.randrange(-100, 101))
            position = (random.randrange(40, window_width - 39), random.randrange(40, window_height - 39))
            body = pymunk.Body(mass = 1, moment = 1000) # dynamic body
            body.position = position
            body.apply_impulse_at_local_point(impulse)
            circle = pymunk.Circle(body, radius = 10)
            circle.elasticity = 1 # all energy = kinetic energy
            circle.friction = 0
            circle.color = (255, 150, 0, 255)
            self.space.add(body, circle)

        # hand segments
        self.no_hand_segments = 21
        self.hand_segments = {}

    def update_hand(self, landmarks, line_paths):
        # delete previous segments
        if len(self.hand_segments) != 0:
            for segment in list(self.hand_segments.keys()):
                self.space.remove(self.hand_segments[segment], segment)
                del self.hand_segments[segment]

        # new hand segments
        for path in line_paths:
            for index in range(len(path) - 1):
                # points
                p0 = Vector(landmarks[path[index]].x * window_width, landmarks[path[index]].y * window_height)
                p1 = Vector(landmarks[path[index + 1]].x * window_width, landmarks[path[index + 1]].y * window_height)
                p0.cartesian()
                p1.cartesian()

                # body
                com = Vector(*get_midpoint(*p0.as_tuple(), *p1.as_tuple())) # center of mass
                body = pymunk.Body(1, 10, pymunk.Body.KINEMATIC)

                # segment
                left = p1
                right = p0
                segment = pymunk.Segment(body, left.as_tuple(), right.as_tuple(), 2)
                segment.elasticity = 1 # all energy = kinetic energy
                segment.color = (245, 230, 225, 255)
                self.hand_segments[segment] = body
                self.space.add(body, segment)
                
