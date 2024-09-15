import pygame
from bird import Bird
from pipe import Pipe
from background import Background
import config
import random

class Game:
    """Main class to handle game logic and loop"""

    def __init__(self):
        """Initialize game and its components"""
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption('Flying Bird Game')
        self.clock = pygame.time.Clock()

        # Initialize game components
        self.bird = Bird(config.BIRD_START_X, config.BIRD_START_Y)
        self.pipes = [Pipe(config.SCREEN_WIDTH + 100)]
        self.background = Background()
        self.pipe_timer = 0  # Track pipe spawn interval
        self.speed_factor = 1.0  # Speed increases over time
        self.score = 0  # Initialize score
        self.font = pygame.font.Font(None, 36)  # Font for score display

    def increase_speed(self):
        """Increase game speed over time"""
        self.speed_factor += 0.001  # Increase the speed factor slowly over time

    def spawn_pipe(self):
        """Generate new pipes at certain intervals"""
        self.pipes.append(Pipe(config.SCREEN_WIDTH + 100))

    def check_collision(self):
        """Check for collisions between bird and pipes or screen edges"""
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.rect_top) or self.bird.rect.colliderect(pipe.rect_bottom):
                hit_sound = pygame.mixer.Sound(config.HIT_SOUND_PATH)
                hit_sound.play()
                return True
        return self.bird.rect.bottom >= config.SCREEN_HEIGHT or self.bird.rect.top <= 0

    def update_score(self):
        """Update the score when the bird passes a pipe"""
        for pipe in self.pipes:
            if pipe.rect_top.right < self.bird.rect.left and not pipe.passed:
                self.score += 1
                pipe.passed = True

    def display_score(self):
        """Display the score on the screen"""
        score_surface = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))

    def run(self):
        """Main game loop"""
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.bird.flap()

            # Increase speed as the game progresses
            self.increase_speed()

            # Game logic
            self.bird.update()
            self.background.move()

            # Adjust pipes' velocity based on speed_factor
            for pipe in self.pipes:
                pipe.move()

            # Check for new pipe generation
            self.pipe_timer += 1
            if self.pipe_timer > 100 / self.speed_factor:  # Spawn pipes faster as speed increases
                self.spawn_pipe()
                self.pipe_timer = 0

            # Update and display score
            self.update_score()

            # Remove pipes that are off-screen
            self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]

            # Check for collision or end game
            if self.check_collision():
                print(f"Game Over! Final Score: {self.score}")
                running = False

            # Draw everything
            self.screen.fill(config.COLOR_BLACK)  # Clear screen
            self.background.draw(self.screen)
            self.bird.draw(self.screen)
            for pipe in self.pipes:
                pipe.draw(self.screen)

            # Display the score
            self.display_score()

            pygame.display.update()
            self.clock.tick(config.FPS)

        pygame.quit()