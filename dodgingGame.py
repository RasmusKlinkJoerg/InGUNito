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
    K_SPACE,
    K_LSHIFT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Colors
red = (255, 0, 0)


# Define constants for the screen width and height
SCREEN_WIDTH = 1700
SCREEN_HEIGHT = 900


def get_random_guy_sprite_path():
    # assign directory
    directory = 'sprites/guys'

    filenames = os.listdir(directory)
    random_file = filenames[random.randint(0, len(filenames) - 1)]
    f = os.path.join(directory, random_file)
    return f


# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        sprite_path = get_random_guy_sprite_path()
        self.surf = pg.image.load(sprite_path).convert_alpha()

        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        self.surf = pg.transform.scale(self.surf, (80, 80))

        self.mask = pg.mask.from_surface(self.surf)

        self.rect = self.surf.get_rect()

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        speed = 5
        if pressed_keys[K_SPACE] or pressed_keys[K_LSHIFT]:
            speed = 10
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -speed)
            move_up_sound.play()
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, speed)
            move_down_sound.play()
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-speed, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(speed, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define the enemy object extending pg.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        sprite_path = get_random_guy_sprite_path()
        self.surf = pg.image.load(sprite_path).convert_alpha()
        self.surf = pg.transform.scale(self.surf, (80, 80))

        self.mask = pg.mask.from_surface(self.surf)

        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 5)

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


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
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
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

# Create custom events for adding a new enemy and cloud
ADDENEMY = pg.USEREVENT + 1
pg.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pg.USEREVENT + 2
pg.time.set_timer(ADDCLOUD, 1000)

# Create our 'player'
player = Player()

line_sprite = Line()

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
enemies = pg.sprite.Group()
clouds = pg.sprite.Group()
all_sprites = pg.sprite.Group()
all_sprites.add(player)
all_sprites.add(line_sprite)

# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pg.mixer.music.load("simplePlaneGame/Apoxode_-_Electric_1.mp3")
pg.mixer.music.play(loops=-1)

# Load all our sound files
# Sound sources: Jon Fincher
move_up_sound = pg.mixer.Sound("simplePlaneGame/Rising_putter.ogg")
move_down_sound = pg.mixer.Sound("simplePlaneGame/Falling_putter.ogg")
collision_sound = pg.mixer.Sound("simplePlaneGame/Collision.ogg")

# Set the base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
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

# Variable to keep our main loop running
running = True

# Our main loop
while running:
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

        # Should we add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Should we add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud, and add it to our sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        # Kill if you click on a guy
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            collision_sound.play()

            pos_in_mask = pos[0] - player.rect.x, pos[1] - player.rect.y
            touching_player = player.rect.collidepoint(*pos) and player.mask.get_at(pos_in_mask)
            if touching_player:
                player.kill()
                print("Suicide!")

            for enemy in enemies:
                pos_in_mask = pos[0] - enemy.rect.x, pos[1] - enemy.rect.y
                touching_enemy = enemy.rect.collidepoint(*pos) and enemy.mask.get_at(pos_in_mask)
                if touching_enemy:
                    enemy.kill()
                    break

    # Get the set of keys pressed and check for user input
    pressed_keys = pg.key.get_pressed()
    player.update(pressed_keys)

    # Update the position of our enemies and clouds
    enemies.update()
    clouds.update()

    # Fill the screen with sky blue
    screen.fill((135, 206, 250))


    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # # Check if any enemies have collided with the player
    for enemy in enemies:
        if pg.sprite.collide_mask(player, enemy):
            # If so, remove the player
            player.kill()
            print("You died.")

            # Stop any moving sounds and play the collision sound
            move_up_sound.stop()
            move_down_sound.stop()
            collision_sound.play()

            # Stop the loop
            running = False


    if pg.sprite.collide_mask(line_sprite, player):
        print("YOU WIN!!!")
        running = False


    # Flip everything to the display
    pg.display.flip()

    # Ensure we maintain a 30 frames per second rate
    clock.tick(60)

# At this point, we're done, so we can stop and quit the mixer
pg.mixer.music.stop()
pg.mixer.quit()
