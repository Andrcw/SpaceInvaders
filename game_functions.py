import sys

from time import sleep
import pygame

from bullet import Bullet, BadBullet
from alien import Alien1, Alien2, Alien3
from random import randint
import math


def check_keydown_events(event, ai_settings, screen, ship, bullets, bad_bullets, aliens):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
        bullets, bad_bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, bad_bullets, aliens)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True
        stats.game_pause = True
        
        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        pygame.mixer.music.load('sounds/shoot.wav')
        pygame.mixer.music.play(0)


def fire_bad_bullet(ai_settings, screen, aliens, bad_bullets):
    if len(bad_bullets) < 6 and len(aliens.sprites()) is not 0:
            new_bad_bullet = BadBullet(ai_settings, screen, aliens)

            last = len(aliens.sprites())
            n = randint(0, last - 1)
            new_bad_bullet.rect.centerx = aliens.sprites()[n].rect.centerx
            new_bad_bullet.rect.centery = aliens.sprites()[n].rect.centery
            new_bad_bullet.y = new_bad_bullet.rect.centery

            ai_settings.timer += .1
            if ai_settings.timer > 5:
                bad_bullets.add(new_bad_bullet)
                pygame.mixer.music.load('sounds/shoot.wav')
                pygame.mixer.music.play(0)
                ai_settings.timer = 0


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, bad_bullets, play_button, bunker):
    """Update images on the screen, and flip to the new screen."""
    # Redraw the screen, each pass through the loop.
    screen.fill(ai_settings.bg_color)
    
    # Redraw all bullets, behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for bad_bullet in bad_bullets.sprites():
        bad_bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    bunker.blitme()
    
    # Draw the score information.
    sb.show_score()
    
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, bad_bullets):
    """Update position of bullets, and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    for bad_bullet in bad_bullets.copy():
        if bad_bullet.rect.bottom >= 800:
            bad_bullets.remove(bad_bullet)


    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets, bad_bullets )


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, bad_bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)

    if collisions:
        for aliens in collisions.values():
            for a in aliens:
                a.boom = True
                stats.score += a.score * len(aliens)
                sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()
        
        # Increase level.
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet, and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    # Empty the list of aliens and bullets.
    # aliens.empty()
    # bullets.empty()

    # Create a new fleet, and center the ship.
    # create_fleet(ai_settings, screen, ship, aliens)
    # ship.center_ship()

    # Pause.
    # sleep(0.5)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, bad_bullets):
    """
    Check if the fleet is at an edge, then update the positions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        pygame.sprite.spritecollideany(ship, bad_bullets).kill()
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # bad bullet and ship collision.
    if pygame.sprite.spritecollideany(ship, bad_bullets):
        pygame.sprite.spritecollideany(ship, bad_bullets).kill()
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
        stats.game_pause = False
        ship.boom = True
        pygame.mixer.music.load('sounds/explosion.wav')
        pygame.mixer.music.play(0)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def create_alien1(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien, and place it in the row."""
    alien = Alien1(ai_settings, screen)
    alien_width = 52
    alien.x = alien_width + 1.7 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.7 * alien.rect.height * row_number
    aliens.add(alien)


def create_alien2(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien, and place it in the row."""
    alien = Alien2(ai_settings, screen)
    alien_width = 52
    alien.x = alien_width + 1.7 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.7 * alien.rect.height * row_number
    aliens.add(alien)


def create_alien3(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien, and place it in the row."""
    alien = Alien3(ai_settings, screen)
    alien_width = 58
    alien.x = alien_width + 1.52 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.7 * alien.rect.height * row_number
    aliens.add(alien)
    # print(aliens.sprites()[1].rect.center)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien, and find number of aliens in a row.
    # alien = Alien1(ai_settings, screen)
    number_aliens_x = 11

    for alien_number in range(number_aliens_x):
        create_alien1(ai_settings, screen, aliens, alien_number, 7)
        create_alien1(ai_settings, screen, aliens, alien_number, 6)
        create_alien2(ai_settings, screen, aliens, alien_number, 5)
        create_alien2(ai_settings, screen, aliens, alien_number, 4)
        create_alien3(ai_settings, screen, aliens, alien_number, 3)
