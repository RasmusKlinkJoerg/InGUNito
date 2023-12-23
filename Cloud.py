
# Import the pygame module
import pygame as pg

# Import pygame.locals for easier access to key coordinates
from pygame.locals import *

# Import random for random numbers
import random

import config
import utilities


# Define constants for the screen width and height
SCREEN_WIDTH = config.SCREEN_WIDTH
SCREEN_HEIGHT = config.SCREEN_HEIGHT

screen = utilities.screen


# Define the cloud object extending pg.sprite.Sprite
# Use an image for a better looking sprite
class Cloud(pg.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pg.image.load("sprites/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                0,
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 5)

    # Move the cloud based on a constant speed
    # Remove it when it passes the right edge of the screen
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right > SCREEN_WIDTH:
            self.kill()