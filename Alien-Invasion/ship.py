import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """ A class representing a singgle instance of a ship."""
    def __init__(self, ai_settings, screen):
        """ Initializing the screen and set it's starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship and get it's rect
        self.image = pygame.image.load("images/ship.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start new ship at the center-bottom of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for ship's center.
        # Pygame rect attributes only store integer values.
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def center_ship(self):
        """Center the ship on the screen."""
        self.centerx = self.screen_rect.centerx
        self.centery = self.screen_rect.bottom - 20

    def update(self):
        """ Update ship's position based on movement flag """
        # Update the ship's center value not the rect.
        if self.moving_right and (self.rect.right < self.screen_rect.right):
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and (self.rect.left > 0):
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_up and (self.rect.top > 0):
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and (self.rect.bottom < self.screen_rect.bottom):
            self.centery += self.ai_settings.ship_speed_factor

        # Update rect value from self.center.
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blitme(self):
        """ Draw the ship at it's current position. """
        self.screen.blit(self.image, self.rect)
