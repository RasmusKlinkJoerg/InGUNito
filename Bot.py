# Import the pygame module
import pygame as pg

import utilities
from utilities import get_random_guy_sprite_path

# Import random for random numbers
import random

# Define constants for the screen width and height
SCREEN_WIDTH = utilities.SCREEN_WIDTH
SCREEN_HEIGHT = utilities.SCREEN_HEIGHT

WALKING_SPEED = utilities.WALKING_SPEED

NUMBER_OF_PLAYERS = utilities.NUMBER_OF_PLAYERS
NUMBER_OF_BOTS = utilities.NUMBER_OF_BOTS

number_of_units = utilities.number_of_units

unit_permutation = utilities.unit_permutation

screen = utilities.screen


# Define the bot object extending pg.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Bot(pg.sprite.Sprite):
    def __init__(self, bot_number):
        super(Bot, self).__init__()
        sprite_path = get_random_guy_sprite_path()
        self.surf = pg.image.load(sprite_path).convert_alpha()
        self.surf = pg.transform.scale(self.surf, (59, 50))
        self.mask = pg.mask.from_surface(self.surf)

        # The starting position
        self.rect = self.surf.get_rect(center=(
            40,  # TODO why does bots x-axis work different than players?
            30 + (SCREEN_HEIGHT / number_of_units) * unit_permutation[bot_number],
        ))

        self.speed = WALKING_SPEED
        self.moving = False

    # Move the bot based on speed
    def update(self):
        start_moving_probability = 0.005
        if random.uniform(0, 1) < start_moving_probability:
            self.moving = True

        stop_moving_probability = 0.05
        if random.uniform(0, 1) < stop_moving_probability:
            self.moving = False

        if self.moving:
            self.rect.move_ip(self.speed, 0)