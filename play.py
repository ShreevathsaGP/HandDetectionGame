# play.py

import cv2
import sys
import math
import time
import pygame
import random
import numpy as np
from globy import *
import mediapipe as mp
from game import Game

# mediapipe
index_finger = 8
no_landmarks = 21
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence = 0.5, min_tracking_confidence = 0.5, max_num_hands = 1)
line_paths = [[0, 1, 2, 3, 4], [0, 5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16], [0, 17, 18, 19, 20], [5, 9, 13, 17]]

# pygame pygame.init()
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Hand Detection Game")

# game [ fps = 30 ]
fps = 30
fps_clock = pygame.time.Clock()
rect = [window_width / 2, window_height / 2, 50, 50]
white = (255, 255, 255)
simple_game = Game()

# time management
previous_time = time.time()
current_time = None

# game loop
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

    # detection & mapping
    window.fill((0,0,0))
    results = hands.process(mp_frame) 
    if results.multi_hand_landmarks :
        x = (sum([results.multi_hand_landmarks[0].landmark[i].x for i in range(no_landmarks)]) / no_landmarks) * window_width
        y = (sum([results.multi_hand_landmarks[0].landmark[i].y for i in range(no_landmarks)]) / no_landmarks) * window_height
        landmarks = results.multi_hand_landmarks[0].landmark

        # render
        for landmark in landmarks:
            pygame.draw.circle(window, white, (landmark.x * window_width, landmark.y * window_height), 15)

        for path in line_paths:
            for index in range(len(path) - 1):
                pygame.draw.line(window, white, 
                        (landmarks[path[index]].x * window_width, landmarks[path[index]].y * window_height),
                        (landmarks[path[index + 1]].x * window_width, landmarks[path[index + 1]].y * window_height), 2)

    # pygame
    pygame.display.update()
    fps_clock.tick(fps)

capture.release()
