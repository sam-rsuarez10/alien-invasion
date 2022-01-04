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

        # Bullet Settings
        self.bullet_speed_factor = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # Alien Settings 
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 2
        # 1 is moving right, -1 is moving left
        self.fleet_direction = 1