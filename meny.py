import pygame
import sys
from Button import Button
from main import run_game

# Inspiration from baraltech - https://www.youtube.com/watch?v=GMBqjxcKogA

pygame.init()

SCREEN_WIDTH = 1280 - 100
SCREEN_HEIGHT = 720 - 100

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

# Load the background image
BG = pygame.image.load("assets/Background.png")

# Resize the background image to fit the screen size
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def play(screen):
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu(screen)

        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu(screen):
    PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3), 
                        text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 
                        text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(SCREEN_WIDTH // 2, 2 * SCREEN_HEIGHT // 3), 
                        text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

    selected_button = 0  # Index of the currently selected button
    buttons = [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]

    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))

        for button in buttons:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for index, button in enumerate(buttons):
                    if button.checkForInput(MENU_MOUSE_POS):
                        if index == 0:
                            run_game()
                        elif index == 1:
                            options()
                        elif index == 2:
                            pygame.quit()
                            sys.exit()
            
            # Handle arrow key navigation
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_button = (selected_button + 1) % len(buttons)
                elif event.key == pygame.K_UP:
                    selected_button = (selected_button - 1) % len(buttons)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    # Perform the action associated with the selected button
                    if selected_button == 0:
                        play(screen)
                    elif selected_button == 1:
                        options()
                    elif selected_button == 2:
                        pygame.quit()
                        sys.exit()

        # Draw a highlight rectangle around the selected button
        selected_button_rect = buttons[selected_button].rect.copy()
        selected_button_rect.inflate_ip(10, 10)
        pygame.draw.rect(SCREEN, (255, 0, 0), selected_button_rect, 2)

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        pygame.display.update()

if __name__ == "__main__":
    main_menu(SCREEN)  # Pass the screen to main_menu()
