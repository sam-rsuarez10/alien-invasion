def fire_bullet(ai_settings, screen, ship, bullets):
    """ Fire a bullet while limit not reached yet """
     # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet =  Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)