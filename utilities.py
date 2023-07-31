import pygame as pg

# Import random for random numbers
import random

import os

# Colors
red = (255, 0, 0)
black = (0, 0, 0)

# Define constants for the screen width and height
SCREEN_WIDTH = 1200#1700
SCREEN_HEIGHT = 700#900

WALKING_SPEED = 2
RUNNING_SPEED = 4

NUMBER_OF_PLAYERS = 4
NUMBER_OF_BOTS = 15

number_of_units = NUMBER_OF_PLAYERS + NUMBER_OF_BOTS

unit_permutation = random.sample(list(range(number_of_units)), number_of_units)

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


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

