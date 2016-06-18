import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, stats, sb, play_button,
                         ship, aliens, bullets):
    """ Respond to keypresses. """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    if event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
    if event.key == pygame.K_q:
        sys.exit()
    if event.key == pygame.K_RETURN:
        if ai_settings.pause_count == 2:
            # Reset the game settings.
            ai_settings.initialize_dynamic_settings()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

            # Reset the game statistics.
            stats.reset_stats()
            stats.game_active = True
            pygame.mouse.set_visible(True)

            # Reset the scoreboard images.
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()

            # Empty the list of aliens and bullets.
            aliens.empty()
            bullets.empty()

            # Create a new fleet.
            create_fleet(ai_settings, screen, ship, aliens)

        elif (ai_settings.pause_count % 2) == 0:
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)
            # Unpause
            stats.game_active = True

        else:
            # Show the mouse cursor.
            pygame.mouse.set_visible(True)

            # Pause game.
            stats.game_active = False

            # Show button.
            play_button.draw_button()

        ai_settings.pause_count += 1


def check_keyup_events(event, ship):
    """ Respond to key releases. """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):
    """ Respond to keypress and mouse events. """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb,
                                 play_button, ship, aliens, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:

        if ai_settings.pause_count <= 2:
            # Reset the game settings.
            ai_settings.initialize_dynamic_settings()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

            # Reset the game statistics.
            stats.reset_stats()
            stats.game_active = True
            pygame.mouse.set_visible(True)

            # Reset the scoreboard images.
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()

            # Empty the list of aliens and bullets.
            aliens.empty()
            bullets.empty()

            # Create a new fleet.
            create_fleet(ai_settings, screen, ship, aliens)
        else:
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)
            # Unpause
            stats.game_active = True

    ai_settings.pause_count += 1


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                  bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    # Change the first boolean value to False for super bullets
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Destroy existing bullets, speed up game, and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()

        # If the entire fleet is destroyed, start a new level.
        stats.level += 1
        sb.prep_level()

        # Center the ship and create a new fleet.
        ship.center_ship()
        create_fleet(ai_settings, screen, ship, aliens)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """ Create an alien and place it on the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Create the first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Create an alien and place it in the row.
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def fire_bullets(ai_settings, screen, ship, bullets):
    """ Fire a bullet if limit is not reached yet. """
    # Create new bullets and add it to the bullets group
    if len(bullets) <= ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """ Determine the total numbers of that fit in a row. """
    # Spacing between each alien is equal to one alien width.
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) -
                         ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

        # Pause.
        sleep(1)
    else:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(True)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = False

        with open('high_score.txt', 'w') as high_score_file:
            high_score_file.write(str(stats.high_score))

    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()

    # Center the ship and create a new fleet.
    ship.center_ship()
    create_fleet(ai_settings, screen, ship, aliens)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button):
    """ Update images on the screen and flip to the new screen """
    # Redraw the screen each time it passes the loop
    screen.fill(ai_settings.bg_color)
    # Redraw all bullets behind the ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make most recently drawn screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Update position of bullets and get rid of old bullets. """
    # Update bullet positions.
    bullets.update()
    # Removing bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                  bullets)


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Check if the fleet is at an edge,
        and then update the postions of all aliens in the fleet.
    """
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
