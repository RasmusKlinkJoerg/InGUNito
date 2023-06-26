# Import the pygame module
import pygame as pg

# Import random for random numbers
import random

import os

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_a,
    K_s,
    K_d,
    K_r,
    K_e,
    K_t,
    K_y,
    K_q,
    K_COMMA,
    K_MINUS,
    K_PERIOD,
    K_SPACE,
    K_LSHIFT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Colors
red = (255, 0, 0)
black = (0, 0, 0)

# Define constants for the screen width and height
SCREEN_WIDTH = 1700
SCREEN_HEIGHT = 900

WALKING_SPEED = 2
RUNNING_SPEED = 4

NUMBER_OF_PLAYERS = 2
NUMBER_OF_BOTS = 15

number_of_units = NUMBER_OF_PLAYERS + NUMBER_OF_BOTS

unit_permutation = random.sample(list(range(number_of_units)), number_of_units)


def get_random_guy_sprite_path():
    # assign directory
    directory = 'sprites/guys'

    filenames = os.listdir(directory)
    random_file = filenames[random.randint(0, len(filenames) - 1)]
    f = os.path.join(directory, random_file)
    return f


def get_scope_path(player_number):
    directory = 'sprites/scopes'
    filenames = os.listdir(directory)
    file = filenames[player_number]
    f = os.path.join(directory, file)
    return f


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
    def update(self, pressed_keys):
        speed = WALKING_SPEED

        # Player 1
        left_key = K_r
        right_key = K_y
        running_key = K_t

        # Player 2
        if self.player_number == 1:
            left_key = K_COMMA
            right_key = K_MINUS
            running_key = K_PERIOD

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


# Define the a gun scope object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Scope(pg.sprite.Sprite):
    def __init__(self, player_number):
        super(Scope, self).__init__()
        sprite_path = get_scope_path(player_number)
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

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        speed = 9

        # Player 1
        left_key = K_a
        right_key = K_d
        up_key = K_w
        down_key = K_s
        shoot_key = K_q

        # Player 2
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

        # Keep scope on the screen
        if self.rect.center[0] < 0:
            self.rect.center = (0, self.rect.center[1])
        elif self.rect.center[0] > SCREEN_WIDTH:
            self.rect.center = self.rect.center = (SCREEN_WIDTH, self.rect.center[1])
        if self.rect.center[1] <= 0:
            self.rect.center = (self.rect.center[0], 0)
        elif self.rect.center[1] >= SCREEN_HEIGHT:
            self.rect.center = (self.rect.center[0], SCREEN_HEIGHT)

        # Shooting
        if pressed_keys[shoot_key] and self.number_of_shots > 0:
            center_pos = self.rect.center
            collision_sound.play()

            for player in players:
                pos_in_mask = center_pos[0] - player.rect.x, center_pos[1] - player.rect.y
                touching_player = player.rect.collidepoint(*center_pos) and player.mask.get_at(pos_in_mask)
                if touching_player:
                    player.kill()
                    break  # break so you can't kill yourself and another with the same shot

            for bot in bots:
                pos_in_mask = center_pos[0] - bot.rect.x, center_pos[1] - bot.rect.y
                touching_bot = bot.rect.collidepoint(*center_pos) and bot.mask.get_at(pos_in_mask)
                if touching_bot:
                    bot.kill()
                    break

            self.number_of_shots -= 1

        # Number of shots
        number_of_shots_display = self.my_font.render(str(self.number_of_shots), True, black)
        screen.blit(number_of_shots_display, (self.rect.bottomleft[0] + 10, self.rect.bottomleft[1] - 10))


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


class Line(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        width = 30
        self.surf = pg.Surface([width, SCREEN_HEIGHT])
        self.rect = self.surf.get_rect()
        self.rect.x = SCREEN_WIDTH - width
        self.rect.y = 0
        self.surf.fill(red)
        self.image = self.surf


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


# Setup for sounds, defaults are good
pg.mixer.init()

# Initialize pg
pg.init()

# Setup the clock for a decent framerate
clock = pg.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create custom events for adding a cloud
ADDCLOUD = pg.USEREVENT + 2
pg.time.set_timer(ADDCLOUD, 1000)

line_sprite = Line()

# Create groups to hold bot sprites, cloud sprites, and all sprites
# - bots is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
bots = pg.sprite.Group()
players = pg.sprite.Group()
scopes = pg.sprite.Group()
clouds = pg.sprite.Group()
all_sprites = pg.sprite.Group()
all_sprites.add(line_sprite)

# Create bots
for i in range(NUMBER_OF_PLAYERS, number_of_units):
    new_bot = Bot(i)
    bots.add(new_bot)
    all_sprites.add(new_bot)

# Create players and scopes
for i in range(0, NUMBER_OF_PLAYERS):
    new_player = Player(i)
    new_scope = Scope(i)

    players.add(new_player)
    scopes.add(new_scope)

    all_sprites.add(new_player)
    all_sprites.add(new_scope)

# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
# pg.mixer.music.load("simplePlaneGame/Apoxode_-_Electric_1.mp3")
# pg.mixer.music.play(loops=-1)

# Load all our sound files
# Sound sources: Jon Fincher
collision_sound = pg.mixer.Sound("simplePlaneGame/Collision.ogg")

# Set the base volume for all sounds
collision_sound.set_volume(0.5)


def set_custom_cursor():
    # Define the size of the cursor
    cursor_size = 32
    # Create a new surface to draw the custom cursor image
    cursor_surf = pg.Surface((cursor_size, cursor_size), pg.SRCALPHA)
    # Draw the circle around the crosshair
    pg.draw.circle(cursor_surf, (255, 255, 255), (cursor_size // 2, cursor_size // 2), cursor_size // 2, 1)
    # Draw the crosshair in the center of the circle
    pg.draw.line(cursor_surf, (255, 255, 255), (cursor_size // 2, 0), (cursor_size // 2, cursor_size))
    pg.draw.line(cursor_surf, (255, 255, 255), (0, cursor_size // 2), (cursor_size, cursor_size // 2))
    cursor3 = pg.cursors.Cursor((15, 5), cursor_surf)
    # Set the cursor to the custom image
    pg.mouse.set_cursor(cursor3)


pg.mouse.set_cursor(pg.SYSTEM_CURSOR_CROSSHAIR)

bg = pg.image.load("background1.jpeg")

# Variable to keep our main loop running
running = True

# Our main loop
while running:

    screen.blit(bg, (0, 0))

    # Look at every event in the queue
    for event in pg.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

        # Should we add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud, and add it to our sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        # Kill if you click on a guy
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            collision_sound.play()

            for player in players:
                pos_in_mask = mouse_pos[0] - player.rect.x, mouse_pos[1] - player.rect.y
                touching_player = player.rect.collidepoint(*mouse_pos) and player.mask.get_at(pos_in_mask)
                if touching_player:
                    player.kill()
                    break  # break so you can't kill yourself and another with the same shot

            for bot in bots:
                pos_in_mask = mouse_pos[0] - bot.rect.x, mouse_pos[1] - bot.rect.y
                touching_bot = bot.rect.collidepoint(*mouse_pos) and bot.mask.get_at(pos_in_mask)
                if touching_bot:
                    bot.kill()
                    break

    # Get the set of keys pressed and check for user input
    pressed_keys = pg.key.get_pressed()
    for player in players:
        player.update(pressed_keys)

        if pg.sprite.collide_mask(line_sprite, player):
            print("Player", player.player_number + 1, "WINS!!!")
            running = False

    # Check if a bot has won
    for bot in bots:
        if pg.sprite.collide_mask(line_sprite, bot):
            print("THE BOT WINS!!!")
            running = False

    for scope in scopes:
        scope.update(pressed_keys)

    # Update the position of our bots and clouds
    bots.update()
    clouds.update()

    # Fill the screen with sky blue.....................
    # screen.fill((135, 206, 250))


    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Flip everything to the display
    pg.display.flip()

    # Ensure we maintain a 30 frames per second rate
    clock.tick(60)

# At this point, we're done, so we can stop and quit the mixer
pg.mixer.music.stop()
pg.mixer.quit()
