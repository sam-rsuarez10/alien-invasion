import pygame 
from settings import Settings
import game_functions as gf

def run_game():
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode(
        (game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption("Exercise 1")

    while True:
        gf.check_events()
        screen.fill(game_settings.bg_color)
        pygame.display.flip()

run_game()

