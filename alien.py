import pygame
from pygame.sprite import Sprite
import math


class Alien1(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen):
        """Initialize the alien, and set its starting position."""
        super(Alien1, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image, and set its rect attribute.
        self.images = []
        self.images.append(pygame.image.load('images/alien1_a.png'))
        self.images.append(pygame.image.load('images/alien1_b.png'))

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left."""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

        self.index += .08
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[math.floor(self.index)]

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)


class Alien2(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen):
        """Initialize the alien, and set its starting position."""
        super(Alien2, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image, and set its rect attribute.
        self.images = []
        self.images.append(pygame.image.load('images/alien2_a.png'))
        self.images.append(pygame.image.load('images/alien2_b.png'))

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left."""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

        # go thru index for animation
        self.index += .08
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[math.floor(self.index)]

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

class Alien3(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen):
        """Initialize the alien, and set its starting position."""
        super(Alien3, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image, and set its rect attribute.
        self.images = []
        self.images.append(pygame.image.load('images/alien3_a.png'))
        self.images.append(pygame.image.load('images/alien3_b.png'))

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left."""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

        # go thru index for animation
        self.index += .08
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[math.floor(self.index)]

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
