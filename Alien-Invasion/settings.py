class Settings():
    """ A class to store all the settings for Alien Invasion. """

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (31, 33, 39)

        # Ship settings
        self.ship_limit = 2

        # Alien settings
        self.fleet_drop_speed = 5

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 255, 255
        self.bullet_allowed = 15

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 2

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Pause count.
        self.pause_count = 2

        # Scoring.
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
