import gym, time
from gym import spaces
import numpy as np
import pygame
import random
import config

class FlyingBirdEnv(gym.Env):
    """Custom Environment that implements the Flying Bird game logic without the Game class"""
    def __init__(self, render=False):
        super(FlyingBirdEnv, self).__init__()
        
        # Action space: 0 - No action, 1 - Flap
        self.action_space = spaces.Discrete(2)

        # Observation space: bird's y position, velocity, nearest pipe's x and y position
        self.observation_space = spaces.Box(
            low=np.array([0, -10, 0, 0], dtype=np.float32),  # y pos, velocity, pipe x, pipe y
            high=np.array([config.SCREEN_HEIGHT, 10, config.SCREEN_WIDTH, config.SCREEN_HEIGHT], dtype=np.float32)
        )

        self.render_enabled = render
        self.screen = None
        self.clock = None
        self.font = None

        self.bird = None
        self.pipes = []
        self.background = None

        self.pipe_timer = 0
        self.speed_factor = 1.0
        self.score = 0
        self.done = False
        self.state = None
        self.info = {}

        if self.render_enabled:
            pygame.init()
            self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            pygame.display.set_caption('Flying Bird Game')
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 36)
        
        self.reset()
    
    def reset(self):
        """Resets the environment to the initial state."""
        # Initialize bird, pipes, and background components
        self.bird = Bird(config.BIRD_START_X, config.BIRD_START_Y, render=self.render_enabled)
        self.pipes = [Pipe(config.SCREEN_WIDTH + 100, render=self.render_enabled)]
        self.background = Background(render=self.render_enabled)
        self.pipe_timer = 0
        self.speed_factor = 1.0
        self.score = 0
        self.done = False
        
        # Get the initial state: bird's position, velocity, nearest pipe's position
        bird_y = self.bird.rect.centery
        bird_vel = self.bird.velocity
        pipe_x = self.pipes[0].rect_top.x
        pipe_y = self.pipes[0].rect_top.height

        self.state = np.array([bird_y, bird_vel, pipe_x, pipe_y], dtype=np.float32)
        self.info = {}
        return self.state
    
    def step(self, action):
        """Executes one time step within the environment."""
        
        # 1. Perform action: If action == 1, bird flaps
        if action == 1:
            self.bird.flap()

        # 2. Update game state
        self.bird.update()
        self.background.move()

        # Move the pipes
        for pipe in self.pipes:
            pipe.move()

        # Check if we need to spawn new pipes
        self.pipe_timer += 1
        if self.pipe_timer > 100 / self.speed_factor:
            self.spawn_pipe()
            self.pipe_timer = 0

        # Update score if the bird passes a pipe
        pipe_passed = self.update_score()

        # Remove pipes that have gone off screen
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]

        # 3. Check for collisions
        done = self.check_collision()

        # 4. Calculate reward
        if done:
            reward = -100  # Negative reward for game over
        elif pipe_passed:
            reward = 1  # Reward for passing a pipe
        else:
            reward = 0  # No reward for just staying in play


        if done:
            self.done = True

        # Bird's y position and velocity
        bird_y = self.bird.rect.centery
        bird_vel = self.bird.velocity

        # Get nearest pipe positions (top and bottom) and distance to it
        if len(self.pipes) > 0:
            pipe = self.pipes[0]
            pipe_x = pipe.rect_top.x
        else:
            pipe_x = config.SCREEN_WIDTH

        # Distance from bird to ground and ceiling
        dist_to_ground = config.SCREEN_HEIGHT - bird_y
        dist_to_ceiling = bird_y

        # Update state
        self.state = np.array([
            bird_y,                # Bird's vertical position
            bird_vel,              # Bird's velocity
            pipe_x - self.bird.rect.x,  # Horizontal distance to the nearest pipe
            dist_to_ground,        # Distance to the ground
            dist_to_ceiling,       # Distance to the ceiling
        ], dtype=np.float32)

        return self.state, reward, self.done, self.info
    
    def spawn_pipe(self):
        """Spawn new pipes at regular intervals."""
        self.pipes.append(Pipe(config.SCREEN_WIDTH + 100, render=self.render_enabled))
        
    def update_score(self):
        """Update the score when the bird passes a pipe and return whether a pipe was passed"""
        for pipe in self.pipes:
            if pipe.rect_top.right < self.bird.rect.left and not pipe.passed:
                self.score += 1
                pipe.passed = True
                return True  # Return True when a pipe is passed
        return False  # Return False if no pipe was passed

    def check_collision(self):
        """Check for collisions between the bird and pipes or screen edges."""
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.rect_top) or self.bird.rect.colliderect(pipe.rect_bottom):
                return True
        return self.bird.rect.bottom >= config.SCREEN_HEIGHT or self.bird.rect.top <= 0
    
    def render(self, mode='human'):
        """Render the current state of the game."""
        if not self.render_enabled or self.done:
            return

        self.screen.fill(config.COLOR_BLACK)  # Clear screen
        self.background.draw(self.screen)
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.display_score()

        pygame.display.update()
        self.clock.tick(config.FPS)
    
    def display_score(self):
        """Display the score on the screen."""
        score_surface = self.font.render(f"Score: {self.score}", True, (0, 0, 255))
        self.screen.blit(score_surface, (10, 10))

    def close(self):
        """Clean up when closing the environment."""
        if self.render_enabled:
            pygame.quit()


class Bird:
    """Class to handle bird properties and behavior"""

    def __init__(self, x: int, y: int, render: bool = True):
        """Initialize bird object with position and velocity"""
        self.render_enabled = render
        if self.render_enabled:
            self.image = pygame.image.load(config.BIRD_IMAGE_PATH).convert_alpha()
            self.image = pygame.transform.scale(self.image, config.BIRD_SCALE)
            pygame.mixer.init()  # Initialize the mixer when render is enabled
            self.flap_sound = pygame.mixer.Sound(config.FLAP_SOUND_PATH)
        else:
            self.flap_sound = None  # No sound when render is disabled
        
        self.rect = pygame.Rect(x, y, *config.BIRD_SCALE)
        self.velocity = 0

    def flap(self):
        """Simulate bird flapping its wings by applying upward velocity."""
        self.velocity = config.FLAP_STRENGTH
        if self.render_enabled:
            self.flap_sound.play()

    def apply_gravity(self):
        """Apply gravity to the bird's movement."""
        self.velocity += config.GRAVITY
        self.rect.centery += self.velocity

    def update(self):
        """Update bird state on every frame."""
        self.apply_gravity()
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom >= config.SCREEN_HEIGHT:
            self.rect.bottom = config.SCREEN_HEIGHT

    def draw(self, screen):
        """Render the bird on the screen."""
        if self.render_enabled:
            screen.blit(self.image, self.rect)


class Pipe:
    """Class to handle pipe properties and movement."""

    def __init__(self, x: int, render: bool = True):
        """Initialize pipe pair (top and bottom) at x-coordinate."""
        self.render_enabled = render
        if self.render_enabled:
            self.image = pygame.image.load(config.PIPE_IMAGE_PATH).convert_alpha()
            self.image = pygame.transform.scale(self.image, config.PIPE_SCALE)
        self.rect_top = pygame.Rect(x, random.randint(100, config.SCREEN_HEIGHT - config.PIPE_GAP - 100), *config.PIPE_SCALE)
        self.rect_bottom = pygame.Rect(x, self.rect_top.bottom + config.PIPE_GAP, config.PIPE_WIDTH, config.SCREEN_HEIGHT)

        self.passed = False

    def move(self):
        """Move the pipe to the left."""
        self.rect_top.x -= config.PIPE_VELOCITY
        self.rect_bottom.x -= config.PIPE_VELOCITY

    def draw(self, screen):
        """Render the pipes."""
        if self.render_enabled:
            screen.blit(self.image, self.rect_top)
            screen.blit(self.image, self.rect_bottom)

    def is_off_screen(self):
        """Check if the pipe has moved off the screen."""
        return self.rect_top.right < 0

class Background:
    """Class to handle background scrolling."""

    def __init__(self, render: bool = True):
        """Initialize background images."""
        self.render_enabled = render
        if self.render_enabled:
            self.image = pygame.image.load(config.BACKGROUND_IMAGE_PATH).convert_alpha()
            self.image = pygame.transform.scale(self.image, config.BACKGROUND_SCALE)
            self.rect1 = self.image.get_rect(topleft=(0, 0))
            self.rect2 = self.image.get_rect(topleft=(config.SCREEN_WIDTH, 0))
        else:
            self.rect1 = pygame.Rect(0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
            self.rect2 = pygame.Rect(config.SCREEN_WIDTH, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

    def move(self):
        """Scroll the background to the left."""
        self.rect1.x -= config.BACKGROUND_VELOCITY
        self.rect2.x -= config.BACKGROUND_VELOCITY
        if self.rect1.right <= 0:
            self.rect1.left = config.SCREEN_WIDTH
        if self.rect2.right <= 0:
            self.rect2.left = config.SCREEN_WIDTH

    def draw(self, screen):
        """Render the background."""
        if self.render_enabled:
            screen.blit(self.image, self.rect1)
            screen.blit(self.image, self.rect2)

if __name__ == "__main__":
    env = FlyingBirdEnv(render=False)
    env.reset()
    done = False
    while not done:
        action = env.action_space.sample()
        # _, _, done, _ = env.step(action)
        state, reward, done, _ = env.step(action)
        # env.render()
        print(f"State: {state}, Reward: {reward}, Done: {done}")
        time.sleep(0.2)
        
    env.close()