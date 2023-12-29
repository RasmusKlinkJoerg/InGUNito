# Import necessary modules
import pygame as pg
from pygame.locals import *

import config
import utilities
from Bot import Bot
from Cloud import Cloud
from FinishLine import FinishLine
from Player import Player
from Scope import Scope

# Constants
NUMBER_OF_PLAYERS = config.NUMBER_OF_PLAYERS
number_of_units = utilities.number_of_units

# Create custom events for adding a cloud
ADDCLOUD = pg.USEREVENT + 2
pg.time.set_timer(ADDCLOUD, 1000)

running = True

def init_joysticks():
    pg.joystick.init()
    joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
    for joystick in joysticks:
        print(joystick.get_name())
    return joysticks


def create_sprites():
    bots = pg.sprite.Group()
    players = pg.sprite.Group()
    scopes = pg.sprite.Group()
    clouds = pg.sprite.Group()
    all_sprites = pg.sprite.Group()
    line_sprite = FinishLine()

    return bots, players, scopes, clouds, line_sprite, all_sprites


def handle_events(joysticks, clouds, players, scopes, bots, all_sprites, player_map, scope_map):
    global running

    # Motion variables for controlling scopes
    motion = [0, 0]
    motion2 = [0, 0]

    # Motion of analog sticks of controllers for moving the scopes,
    # and cut off at thresholds to remove slow drifting that can happen even when analog sticks are not touched
    if abs(motion[0]) < 0.1:
        motion[0] = 0
    if abs(motion[1]) < 0.1:
        motion[1] = 0

    if abs(motion2[0]) < 0.1:
        motion2[0] = 0
    if abs(motion2[1]) < 0.1:
        motion2[1] = 0

    motions = [motion, motion2]

    for i, js in enumerate(joysticks):
        player_map[i].update(player_walking=js.get_button(0), player_running=js.get_button(3))
        # Shooting with left or right bumper button (i.e L1/LB and R1/RB)
        # on PS4 controllers it is js.get_button(9) or js.get_button(10)
        # on Xbox 360 controllers it is js.get_button(4) or js.get_button(5)
        shooting = js.get_button(4) or js.get_button(5) or js.get_button(9) or js.get_button(10)
        scope_map[i].update(players, bots, scopes, scope_motion=motions[i], shooting=shooting)

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

        # Should we add a new cloud?-----------
        elif event.type == ADDCLOUD:
            # Create the new cloud, and add it to our sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)


        elif event.type == JOYBUTTONDOWN:
            print(event)

        elif event.type == JOYAXISMOTION:

            if pg.joystick.Joystick(0).get_axis(0):
                print(event)
                if event.axis < 2:
                    motion[event.axis] = event.value
            if pg.joystick.Joystick(1).get_button(0):
                print(event)
                if event.axis < 2:
                    motion2[event.axis] = event.value

            motion = [joysticks[0].get_axis(0), pg.joystick.Joystick(0).get_axis(1)]
            motion2 = [joysticks[1].get_axis(0), pg.joystick.Joystick(1).get_axis(1)]

        elif event.type == JOYHATMOTION:
            print(event)
        elif event.type == CONTROLLER_AXIS_TRIGGERRIGHT or CONTROLLER_AXIS_TRIGGERLEFT:
            print(event)
        elif event.type == JOYDEVICEADDED:
            joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
            for joystick in joysticks:
                print(joystick.get_name())
        elif event.type == JOYDEVICEREMOVED:
            joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]



def update_game_state(players, bots, scopes, clouds, line_sprite, all_sprites, screen):
    global running

    # Update players controlled by keyboard. Get the set of keys pressed and check for user input
    pressed_keys = pg.key.get_pressed()
    for player in players:
        player.update(pressed_keys)

        # Check if a player has won
        if pg.sprite.collide_mask(line_sprite, player):
            print("Player", player.player_number + 1, "WINS!!!")
            running = False

    # Check if a bot has won
    for bot in bots:
        if pg.sprite.collide_mask(line_sprite, bot):
            print("THE BOT WINS!!!")
            running = False

    # Update scopes controlled with keyboard
    for scope in scopes:
        scope.update(players, bots, scopes, pressed_keys)

    # Update the position of our bots and clouds
    bots.update()
    clouds.update()

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Flip everything to the display
    pg.display.flip()


def initialize_sprites(all_sprites, bots, players, scopes, line_sprite):
    # Create finish line and add bots, players, scopes

    ## Create custom events for adding a cloud
    ADDCLOUD = pg.USEREVENT + 2
    pg.time.set_timer(ADDCLOUD, 1000)

    all_sprites.add(line_sprite)

    # Create bots
    for i in range(NUMBER_OF_PLAYERS, number_of_units):
        new_bot = Bot(i)
        bots.add(new_bot)
        all_sprites.add(new_bot)

    # Create dictionaries of players and scopes
    # and tie each pair together by using the same int as keys in the two dictionaries
    player_map = {}
    scope_map = {}
    for i in range(0, NUMBER_OF_PLAYERS):
        new_player = Player(i)
        new_scope = Scope(i)

        players.add(new_player)
        scopes.add(new_scope)

        player_map[i] = new_player
        scope_map[i] = new_scope

        all_sprites.add(new_player)
        all_sprites.add(new_scope)

    return player_map, scope_map


def main():
    # Initialization
    global running
    pg.init()
    clock = pg.time.Clock()
    screen = utilities.screen
    joysticks = init_joysticks()
    bots, players, scopes, clouds, line_sprite, all_sprites = create_sprites()
    player_map, scope_map = initialize_sprites(all_sprites, bots, players, scopes, line_sprite)
    bg = pg.image.load("background1.jpeg")

    print(running)


    # Main game loop
    while running:
        screen.blit(bg, (0, 0))
        handle_events(joysticks, clouds, players, scopes, bots, all_sprites, player_map, scope_map)
        update_game_state(players, bots, scopes, clouds, line_sprite, all_sprites, screen)

        pg.display.flip()
        clock.tick(60)

    # Cleanup
    pg.mixer.music.stop()
    pg.mixer.quit()


if __name__ == "__main__":
    main()
