import pygame
import random
import config

class Pipe:
    """Class to handle pipe properties and movement"""

    def __init__(self, x: int):
        """Initialize pipe pair (top and bottom) at x-coordinate"""
        self.image = pygame.image.load(config.PIPE_IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.scale(self.image, config.PIPE_SCALE)  # Rescale pipe image
        self.rect_top = self.image.get_rect(midbottom=(x, random.randint(100, config.SCREEN_HEIGHT - config.PIPE_GAP - 100)))
        self.rect_bottom = self.image.get_rect(midtop=(x, self.rect_top.bottom + config.PIPE_GAP))
        self.passed = False  # Track if the bird has passed this pipe

    def move(self):
        """Move the pipe to the left"""
        self.rect_top.x -= config.PIPE_VELOCITY
        self.rect_bottom.x -= config.PIPE_VELOCITY

    def draw(self, screen):
        """Draw top and bottom pipes if rendering is enabled"""
        if screen is not None:
            screen.blit(self.image, self.rect_top)
            screen.blit(self.image, self.rect_bottom)

    def is_off_screen(self):
        """Check if the pipe has moved completely off the screen"""
        return self.rect_top.right < 0