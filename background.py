import pygame
import config

class Background:
    """Class to handle the background scrolling effect"""

    def __init__(self):
        """Initialize two background images for smooth transition"""
        self.image = pygame.image.load(config.BACKGROUND_IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.scale(self.image, config.BACKGROUND_SCALE)  # Rescale background image
        self.rect1 = self.image.get_rect(topleft=(0, 0))
        self.rect2 = self.image.get_rect(topleft=(config.SCREEN_WIDTH, 0))

    def move(self):
        """Scroll the background to the left"""
        self.rect1.x -= config.BACKGROUND_VELOCITY
        self.rect2.x -= config.BACKGROUND_VELOCITY

        # Reset position to create endless scrolling
        if self.rect1.right <= 0:
            self.rect1.left = config.SCREEN_WIDTH
        if self.rect2.right <= 0:
            self.rect2.left = config.SCREEN_WIDTH

    def draw(self, screen):
        """Render both background images for scrolling effect, if rendering is enabled"""
        if screen is not None:
            screen.blit(self.image, self.rect1)
            screen.blit(self.image, self.rect2)