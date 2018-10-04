import pygame

import pygame.sysfont


class Start:
    def __init__(self, screen):
        screen.fill((0, 0, 0))
        self.title = pygame.font.SysFont("monospace", 150)
        self.sub = pygame.font.SysFont("monospace", 80)
        self.medium = pygame.font.SysFont("monospace", 40)

        self.white = (255, 255, 255)
        self.green = (50, 255, 50)
        self.red = (255, 0, 0)

        # for SPACE
        self.space = self.title.render("SPACE", True, self.white)
        self.space_btn = self.space.get_rect()
        self.space_btn.centerx = screen.get_rect().centerx
        self.space_btn.centery = screen.get_rect().centery - 200

    def start_blit(self, screen):
        # Blit text
        screen.blit(self.space, self.space_btn)

        # Display
        pygame.display.flip()

    def start_update(self, ball):
        """ nothing for now. """
