import pygame
import math
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the ship, and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image, and set its rect attribute.
        self.images = []
        self.images.append(pygame.image.load('images/ship.png'))
        self.images.append(pygame.image.load('images/ship2.png'))
        self.images.append(pygame.image.load('images/ship3.png'))
        self.images.append(pygame.image.load('images/ship4.png'))
        self.images.append(pygame.image.load('images/ship5.png'))
        self.images.append(pygame.image.load('images/ship6.png'))
        self.images.append(pygame.image.load('images/ship7.png'))
        self.images.append(pygame.image.load('images/ship8.png'))

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 20
        
        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)
        
        # Movement flags.
        self.moving_right = False
        self.moving_left = False

        self.boom = False


    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx
        
    def update(self, stats):
        """Update the ship's position, based on movement flags."""
        # Update the ship's center value, not the rect.
        if stats.game_pause:
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.center += self.ai_settings.ship_speed_factor
            if self.moving_left and self.rect.left > 0:
                self.center -= self.ai_settings.ship_speed_factor
            
        # Update rect object from self.center.
        self.rect.centerx = self.center

        # Get ship to blow up
        if self.boom:
            self.index += .1
            if self.index >= len(self.images):
                self.index = 0
                self.boom = False
                stats.game_pause = True
            self.image = self.images[math.floor(self.index)]


    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

