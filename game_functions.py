import sys 
import pygame 
from bullet import Bullet
from alien import Alien
from time import sleep


def fire_bullet(ai_settings, screen, ship, bullets):
    """ Fire a bullet while limit not reached yet """
     # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet =  Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keydown_events(event, ai_settings, screen, ship, bullets, aliens, stats):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
       fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, aliens, ship, bullets, stats)

def start_game(ai_settings, screen, aliens , ship, bullets, stats):
    ''' Sets initial parameters to start a new game '''
    ai_settings.initialize_dynamic_settings()
    pygame.mouse.set_visible(False)
    # Reset game statistics
    stats.reset_stats()
    stats.game_active = True

    # Empty the list of aliens and bullets
    aliens.empty()
    bullets.empty()

    # Create new fleet and center the ship
    create_fleet(ai_settings, screen, aliens, ship)
    ship.center_ship()

def check_keyup_events(event, ship):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_play_button(ai_settings, screen, stats, play_button, mouse_x, mouse_y, aliens, bullets, ship):
    ''' Starts a new game when the player clicks Play '''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings
        start_game(ai_settings, screen, aliens, ship, bullets, stats)

def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event, ai_settings, screen, ship, bullets, aliens, stats)
            elif event.type == pygame.KEYUP:
                check_keyup_events(event, ship)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats, play_button, mouse_x, mouse_y, aliens, bullets, ship)


def update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, sb):
    """Update images on the screen and flip to the new screen"""

    # Redraw the screen each gpass through the loop
    screen.fill(ai_settings.bg_color)
    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible
    pygame.display.flip()
# end def

def check_bullet_alien_colissions(bullets, aliens, ai_settings, screen, ship, stats, sb):
    '''Respond to alien-bullet colissions'''
     # Check if a bullet hit an alien
    # If so, delete both bullet and alien
    colissions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if colissions:
        stats.score += ai_settings.alien_points
        sb.prep_score()

    if len(aliens) == 0:
        # Destroy existing bullets, speed up game, and create new fleet
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, aliens, ship)
    # end if
#end def
def update_bullets(bullets, aliens, ai_settings, screen, ship, stats, sb):
    """ Update position of bullets and get rid of old bullets """
    # Update bullet position
    bullets.update()

    # Get rid of the bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #end for
    check_bullet_alien_colissions(bullets, aliens, ai_settings, screen, ship, stats, sb)
# end def

def get_number_aliens_x(ai_settings, alien_width):
    ''' Determine number of aliens that fit in a row '''
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    ''' Determine number of rows of aliens that fit on the screen '''
    available_space_y = (ai_settings.screen_height - (3*alien_height) - ship_height)
    number_rows = int(available_space_y / (2*alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
     # Create an alien and place it in the row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
    alien.rect.x = alien.x
    alien.add(aliens)

def create_fleet(ai_settings, screen, aliens, ship):
    ''' Create a full fleet of aliens '''
    # Create an alien and find the number of aliens in a row 
    # Spacing between each alien is equal to one alien width
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)



def change_fleet_direction(ai_settings, aliens):
    """ Drop entire fleet and change fleet's direction """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    # end for
    if ai_settings.fleet_direction == 'right': # direction is set to right
        ai_settings.set_fleet_direction('left') # set to left  
    else:
        ai_settings.set_fleet_direction('right')
# end def

def check_fleet_edges(ai_settings, aliens):
    ''' Respond appropiately if any alien 
        have reached the edge of screen '''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
    # end for
# end def

def update_aliens(ai_settings, aliens, ship, stats, screen, bullets):
    ''' Check if any alien have reached the edge and update positions of all aliens in the fleet '''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    
    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
# end def

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """ Respond to ship being hit by alien """
    if stats.ships_left > 0:
        # Decrement ships left
        stats.ships_left -= 1

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create new ship and center the ship
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break