"""
Andrew Nguyen
andrew96nguyen@csu.fullerton.edu
Space Invaders
"""

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf
from start import Start


def run_game():

    clock = pygame.time.Clock()

    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")

    # Start
    start = Start(screen)
    
    # Create an instance to store game statistics, and a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    bad_bullets = Group()
    aliens = Group()
    bunkers = Group()
    
    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Create bunkers
    gf.create_bunkers(ai_settings, screen, bunkers)

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, bad_bullets, bunkers)

        if stats.game_active and stats.game_pause:
            # ship.update()
            bad_bullets.update()
            gf.fire_bad_bullet(ai_settings, screen, aliens, bad_bullets)
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers, bad_bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, bad_bullets)

        ship.update(stats)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, bad_bullets, play_button, bunkers, start)
        clock.tick(60)

run_game()
