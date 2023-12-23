# Import the pygame module
import pygame as pg

# Import pygame.locals for easier access to key coordinates
from pygame.locals import *

import config
import utilities
from utilities import get_random_guy_sprite_path


# Define constants for the screen width and height
SCREEN_WIDTH = config.SCREEN_WIDTH
SCREEN_HEIGHT = config.SCREEN_HEIGHT

WALKING_SPEED = config.WALKING_SPEED
RUNNING_SPEED = config.RUNNING_SPEED

number_of_units = utilities.number_of_units

unit_permutation = utilities.unit_permutation


# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Player(pg.sprite.Sprite):
    def __init__(self, player_number):
        super(Player, self).__init__()
        sprite_path = get_random_guy_sprite_path()
        self.surf = pg.image.load(sprite_path).convert_alpha()
        self.surf = pg.transform.scale(self.surf, (59, 50))
        self.mask = pg.mask.from_surface(self.surf)
        self.player_number = player_number

        # Starting position
        self.rect = self.surf.get_rect(center=(
            20,
            30 + (SCREEN_HEIGHT / number_of_units) * unit_permutation[player_number],
        ))

    # Move the sprite based on keypresses
    def update(self, pressed_keys=None, player_walking=False, player_running=False):
        if pressed_keys is None:
            pressed_keys = []

        speed = WALKING_SPEED

        ####################################
        # Players controlled with Joystick #
        ####################################
        if player_running:
            speed = RUNNING_SPEED
            self.rect.move_ip(speed, 0)
        elif player_walking:
            self.rect.move_ip(speed, 0)

        ####################################
        # Players controlled with Keyboard #
        ####################################
        if len(pressed_keys) > 0:
            # Player 1
            left_key = K_COMMA
            right_key = K_MINUS
            running_key = K_PERIOD

            # Player 2
            if self.player_number == 2:
                left_key = K_r
                right_key = K_y
                running_key = K_t

            if pressed_keys[running_key]:
                speed = RUNNING_SPEED

            if pressed_keys[left_key]:
                self.rect.move_ip(-speed, 0)
            if pressed_keys[right_key]:
                self.rect.move_ip(speed, 0)

            # if pressed_keys[K_UP] or pressed_keys[K_w]:
            #     self.rect.move_ip(0, -speed)
            # if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            #     self.rect.move_ip(0, speed)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
