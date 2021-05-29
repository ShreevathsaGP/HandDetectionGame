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

# mediapipe
index_finger = 8
no_landmarks = 21
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence = 0.5, min_tracking_confidence = 0.5, max_num_hands = 1)

# pygame
pygame.init()
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Virtual Breakout")

# game [ fps = 30 ]
fps = 30
fps_clock = pygame.time.Clock()
rect = [window_width / 2, window_height / 2, 30, 30]
white = (255, 255, 255)

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

    # detection
    results = hands.process(mp_frame) 
    if results.multi_hand_landmarks:
        rect[0] = (sum([results.multi_hand_landmarks[0].landmark[i].x for i in range(no_landmarks)]) / no_landmarks) * window_width
        rect[1] = (sum([results.multi_hand_landmarks[0].landmark[i].y for i in range(no_landmarks)]) / no_landmarks) * window_height

    # render
    window.fill((0,0,0))
    pygame.draw.rect(window, white, tuple(rect))
    pygame.display.update()
    fps_clock.tick(fps)

capture.release()
