import pygame
import config

class Bird:
    """Class to handle bird properties and behavior"""

    def __init__(self, x: int, y: int):
        """Initialize bird object with position and velocity"""
        self.image = pygame.image.load(config.BIRD_IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.scale(self.image, config.BIRD_SCALE)  # Rescale bird image
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0
        self.flap_sound = pygame.mixer.Sound(config.FLAP_SOUND_PATH)

    def flap(self):
        """Simulate bird flapping its wings by applying upward velocity"""
        self.velocity = config.FLAP_STRENGTH
        self.flap_sound.play()

    def apply_gravity(self):
        """Apply gravity to the bird's movement"""
        self.velocity += config.GRAVITY
        self.rect.centery += self.velocity

    def update(self):
        """Update bird state on every frame"""
        self.apply_gravity()

        # Prevent bird from going off-screen vertically
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom >= config.SCREEN_HEIGHT:
            self.rect.bottom = config.SCREEN_HEIGHT

    def draw(self, screen):
        """Render the bird on the screen if rendering is enabled"""
        if screen is not None:
            screen.blit(self.image, self.rect)