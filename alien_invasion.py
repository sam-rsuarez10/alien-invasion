import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf 
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # Initialize game, settings and screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the play button
    play_button = Button(ai_settings, screen, "Play")


    # Create an instance to store game statistics
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # Make a ship
    ship = Ship(ai_settings, screen)

    # Make a group to store bullets in
    bullets = Group()

    # Make a group of aliens
    aliens = Group()

    # Create fleet of aliens
    gf.create_fleet(ai_settings, screen, aliens, ship)

    # Start the main loop for the game
    while True:
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb)

        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, ai_settings, screen, ship, stats, sb)
            gf.update_aliens(ai_settings, aliens, ship, stats, screen, bullets, sb)

        gf.update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, sb)



run_game()