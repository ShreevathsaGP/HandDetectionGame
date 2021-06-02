# simulate.py

import cv2
import sys
import math
import time
import pygame
import pymunk
import random
import numpy as np
from globy import *
import mediapipe as mp
from environment import Environment

# mediapipe
index_finger = 8
no_landmarks = 21
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence = 0.5, min_tracking_confidence = 0.5, max_num_hands = 1)
line_paths = [[0, 1, 2, 3, 4], [0, 5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16], [0, 17, 18, 19, 20], [5, 9, 13, 17]]

# pygame 
pygame.init()
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Hand Detection Game")

# others
white = (255, 255, 255)
rect = [window_width / 2, window_height / 2, 50, 50]

# time management
fps = 30
current_time = None
previous_time = time.time()
fps_clock = pygame.time.Clock()

# simulation
pymunk.pygame_util.positive_y_is_up = True
drawing_utils = pymunk.pygame_util.DrawOptions(window)
physics_environment = Environment()

# simulation loop
capture = cv2.VideoCapture(0)
running = True
while capture.isOpened() and running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False

    # capture frame
    ret, frame = capture.read()
    if not ret: continue
    mp_frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    mp_frame.flags.writeable = False # reference pass speedup

    # hand render
    window.fill((0,0,0))
    results = hands.process(mp_frame) 
    if results.multi_hand_landmarks :
        x = (sum([results.multi_hand_landmarks[0].landmark[i].x for i in range(no_landmarks)]) / no_landmarks) * window_width
        y = (sum([results.multi_hand_landmarks[0].landmark[i].y for i in range(no_landmarks)]) / no_landmarks) * window_height
        landmarks = results.multi_hand_landmarks[0].landmark

        # render
        for landmark in landmarks:
            pygame.draw.circle(window, white, (landmark.x * window_width, landmark.y * window_height), 5)

        # hand segments
        physics_environment.update_hand(landmarks, line_paths)

    # env render
    physics_environment.space.debug_draw(drawing_utils)
    physics_environment.space.step(0.01)

    # pygame
    pygame.display.update()
    fps_clock.tick(fps)

capture.release()
