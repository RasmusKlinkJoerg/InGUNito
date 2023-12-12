import pygame
from pygame.examples.joystick import TextPrint

pygame.init()
pygame.display.set_caption("My Game")
screen = pygame.display.set_mode((480, 720))
clock = pygame.time.Clock()
textPrint = TextPrint()
player1 = {'width': 40, 'height': 40, 'velocity': 5, 'color': (0, 200, 255), 'x': 50, 'y': 50}
player2 = {'width': 40, 'height': 40, 'velocity': 5, 'color': (200, 200, 255), 'x': 50, 'y': 50}
run = True
while run:
    #
    # EVENT PROCESSING STEP
    #
    for event in pygame.event.get():  # User did something.
        if event.type == pygame.QUIT:  # If user clicked close.
            run = False  # Flag that we are done so we exit this loop.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False
            #
    # DRAWING STEP
    #
    # First, clear the screen to white. Don't put other drawing commands above this, or they will be erased with this command.
    screen.fill((255,255,255))
    textPrint.reset()
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
    textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))

    if joystick_count >= 1:
        pygame.draw.rect(screen, player1['color'], (player1['x'], player1['y'], player1['width'], player1['height']))
        joystick1 = pygame.joystick.Joystick(0)
        if joystick1.get_axis(0) and joystick1.get_axis(0) < -0.2:
            print(joystick1.get_axis(0))
            player1['x'] -= player1['velocity']
        if joystick1.get_axis(0) and joystick1.get_axis(0) > 0.2:
            player1['x'] += player1['velocity']
        if joystick1.get_axis(1) and joystick1.get_axis(1) < -0.2:
            player1['y'] -= player1['velocity']
        if joystick1.get_axis(1) and joystick1.get_axis(1) > 0.2:
            player1['y'] += player1['velocity']

    if joystick_count > 1:
        pygame.draw.rect(screen, player2['color'], (player2['x'], player2['y'], player2['width'], player2['height']))
        joystick2 = pygame.joystick.Joystick(1)
        if joystick2.get_axis(0) and joystick2.get_axis(0) < -0.2:
            print(joystick2.get_axis(0))

            player2['x'] -= player2['velocity']
        if joystick2.get_axis(0) and joystick2.get_axis(0) > 0.2:
            player2['x'] += player2['velocity']
        if joystick2.get_axis(1) and joystick2.get_axis(1) < -0.2:
            player2['y'] -= player2['velocity']
        if joystick2.get_axis(1) and joystick2.get_axis(1) > 0.2:
            player2['y'] += player2['velocity']