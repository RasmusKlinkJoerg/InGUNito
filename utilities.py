import pygame as pg

import config

# Import random for random numbers
import random

import os

# Colors
red = (255, 0, 0)
black = (0, 0, 0)



number_of_units = config.NUMBER_OF_PLAYERS + config.NUMBER_OF_BOTS

unit_permutation = random.sample(list(range(number_of_units)), number_of_units)

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))


# Setup for sounds, defaults are good
pg.mixer.init()

# Load all our sound files
# Sound sources: Jon Fincher
collision_sound = pg.mixer.Sound("simplePlaneGame/Collision.ogg")
# Set the base volume for all sounds
collision_sound.set_volume(0.5)


def get_random_guy_sprite_path():
    # assign directory
    directory = 'sprites/guys'

    filenames = os.listdir(directory)
    random_file = filenames[random.randint(0, len(filenames) - 1)]
    path = os.path.join(directory, random_file)
    return path


def get_scope_path(player_number):
    directory = 'sprites/scopes'
    filenames = os.listdir(directory)
    file = filenames[player_number]
    path = os.path.join(directory, file)
    return path

