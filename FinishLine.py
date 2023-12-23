
# Import the pygame module
import pygame as pg

import config
import utilities
from utilities import get_random_guy_sprite_path

# Colors
red = utilities.red

# Define constants for the screen width and height
SCREEN_WIDTH = config.SCREEN_WIDTH
SCREEN_HEIGHT = config.SCREEN_HEIGHT


class FinishLine(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        width = 30
        self.surf = pg.Surface([width, SCREEN_HEIGHT])
        self.rect = self.surf.get_rect()
        self.rect.x = SCREEN_WIDTH - width
        self.rect.y = 0
        self.surf.fill(red)
        self.image = self.surf