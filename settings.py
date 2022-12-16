class Settings():
    """ A class to store all settings for alien invasion """
    def __init__(self):
        """Initialize the game's settings """
        # Screen settings
        self.screen_width = 1500
        self.screen_height = 750
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        # Bullet Settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # Alien Settings 
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 'right'
    # end def

    def set_fleet_direction(self, dir):
        self.fleet_direction = dir
    # end def