# Import the pygame module
import pygame as pg

# Import pygame.locals for easier access to key coordinates
from pygame.locals import *

import utilities


# Colors
red = utilities.red
black = utilities.black

# Define constants for the screen width and height
SCREEN_WIDTH = utilities.SCREEN_WIDTH
SCREEN_HEIGHT = utilities.SCREEN_HEIGHT

NUMBER_OF_PLAYERS = utilities.NUMBER_OF_PLAYERS

screen = utilities.screen

collision_sound = utilities.collision_sound


# Define the a gun scope object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Scope(pg.sprite.Sprite):
    def __init__(self, player_number):
        super(Scope, self).__init__()
        sprite_path = utilities.get_scope_path(player_number)
        self.surf = pg.image.load(sprite_path)

        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        self.surf = pg.transform.scale(self.surf, (80, 80))
        self.mask = pg.mask.from_surface(self.surf)
        self.player_number = player_number

        # Starting position
        self.rect = self.surf.get_rect(center=(
            300,
            30 + (SCREEN_HEIGHT / NUMBER_OF_PLAYERS) * player_number,
        ))

        # Number of shots
        self.my_font = pg.font.SysFont("Times New Roman", 18)
        self.number_of_shots = 1

    # Move the sprite based on joysticks and keyboard
    # TODO make more elegant solution with a method with less parameters
    def update(self, players, bots, scopes, pressed_keys=None, scope_motion=None, shooting=False):
        if pressed_keys is None:
            pressed_keys = []
        if scope_motion is None:
            scope_motion = [0, 0]

        speed = 9

        ############################################
        # Players' scopes controlled with Joystick #
        ############################################
        self.rect.move_ip(scope_motion[0] * speed, scope_motion[1] * speed)

        ############################################
        # Players' scopes controlled with keyboard #
        ############################################
        if len(pressed_keys) > 0:
            # keyboard Player 1
            left_key = K_a
            right_key = K_d
            up_key = K_w
            down_key = K_s
            shoot_key = K_q

            # keyboard Player 2
            if self.player_number == 1:
                left_key = K_LEFT
                right_key = K_RIGHT
                up_key = K_UP
                down_key = K_DOWN
                shoot_key = K_SPACE

            if pressed_keys[left_key]:
                self.rect.move_ip(-speed, 0)
            if pressed_keys[right_key]:
                self.rect.move_ip(speed, 0)
            if pressed_keys[up_key]:
                self.rect.move_ip(0, -speed)
            if pressed_keys[down_key]:
                self.rect.move_ip(0, speed)

            if pressed_keys[shoot_key]:
                shooting = True

        # Keep scope on the screen
        if self.rect.center[0] < 0:
            self.rect.center = (0, self.rect.center[1])
        elif self.rect.center[0] > SCREEN_WIDTH:
            self.rect.center = self.rect.center = (SCREEN_WIDTH, self.rect.center[1])
        if self.rect.center[1] <= 0:
            self.rect.center = (self.rect.center[0], 0)
        elif self.rect.center[1] >= SCREEN_HEIGHT:
            self.rect.center = (self.rect.center[0], SCREEN_HEIGHT)

        ############
        # Shooting #
        ############
        if shooting and self.number_of_shots > 0:
            center_pos = self.rect.center

            collision_sound.play()

            # Check if a players has been shot
            for player in players:
                pos_in_mask = center_pos[0] - player.rect.x, center_pos[1] - player.rect.y
                touching_player = player.rect.collidepoint(center_pos) and player.mask.get_at(pos_in_mask)
                if touching_player:
                    player.kill()

                    # Remove the scope of the killed player
                    for scope in scopes:
                        if scope.player_number == player.player_number:
                            scope.kill()
                            scope.number_of_shots = 0

                    break  # break so you can't kill multiple units with the same shot

            # Check if a bot has been shot
            for bot in bots:
                pos_in_mask = center_pos[0] - bot.rect.x, center_pos[1] - bot.rect.y
                touching_bot = bot.rect.collidepoint(*center_pos) and bot.mask.get_at(pos_in_mask)
                if touching_bot:
                    bot.kill()
                    break

            self.number_of_shots -= 1

        # Display the number of shots (i.e. bullets) remaining
        number_of_shots_display = self.my_font.render(str(self.number_of_shots), True, black)
        screen.blit(number_of_shots_display, (self.rect.bottomleft[0] + 10, self.rect.bottomleft[1] - 10))

