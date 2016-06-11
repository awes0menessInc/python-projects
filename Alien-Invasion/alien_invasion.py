import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    """ Main module to run the game."""
    # Initialize pygame, Settings and screen objects
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make the Play button.
    play_button = Button(screen, "Play")

    # Make a ship, group of bullets and group of aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Create a fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Starting main loop for the game
    while True:

        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets)

        if stats.game_active:
            bullets.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                              bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                             bullets)
            ship.update()

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                         play_button)

run_game()
