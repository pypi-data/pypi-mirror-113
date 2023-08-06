import math
import os
import pygame

SANDBOX_WIDTH = 800
SANDBOX_HEIGHT = 600

MARGIN = 12

SANDBOX_X = MARGIN
SANDBOX_Y = MARGIN * 2

WINDOW_WIDTH = SANDBOX_WIDTH + (MARGIN * 2)
WINDOW_HEIGHT = SANDBOX_HEIGHT + (MARGIN * 4) + math.floor(SANDBOX_HEIGHT * 0.3)

MENU_WIDTH = 828
MENU_HEIGHT = 828

MODE = "A"

FPS = 60
PARTICLE_SIZE = 4

FONT_PATH = os.path.join(os.path.dirname(__file__), 'fonts', 'RetroGaming.ttf')  # "fonts/RetroGaming.ttf"
FONT_COLOR = (255, 255, 255)

BG_COLOR = (33, 33, 33)
SANDBOX_COLOR = (0, 0, 0)

TOMENU_EVENT_TYPE = pygame.USEREVENT + 1
TOMENU_EVENT = pygame.event.Event(TOMENU_EVENT_TYPE,)
