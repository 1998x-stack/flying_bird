import gym, time
from gym import spaces
import numpy as np
import pygame
from game import Game
import config

class FlyingBirdEnv(gym.Env):
    """Custom Environment that follows gym interface for the Flying Bird Game"""
    
    def __init__(self, render=False):
        super(FlyingBirdEnv, self).__init__()
        
        # Action space: 0 - No action, 1 - Flap
        self.action_space = spaces.Discrete(2)

        # Observation space: bird's y position, velocity, nearest pipe's x and y position
        self.observation_space = spaces.Box(
            low=np.array([0, -10, 0, 0], dtype=np.float32),  # y pos, velocity, pipe x, pipe y
            high=np.array([config.SCREEN_HEIGHT, 10, config.SCREEN_WIDTH, config.SCREEN_HEIGHT], dtype=np.float32)
        )

        # Initialize the game
        self.render_enabled = render
        self.game = None
        self.state = None
        self.done = False
        self.info = {}
    
    def reset(self):
        """Resets the environment to the initial state."""
        # Reset the game
        if self.game is None:
            self.game = Game(render=self.render_enabled)
        else:
            self.game = Game(render=self.render_enabled)

        # Get the initial state: bird's position, velocity, nearest pipe's position
        bird_y = self.game.bird.rect.centery
        bird_vel = self.game.bird.velocity
        pipe_x = self.game.pipes[0].rect_top.x
        pipe_y = self.game.pipes[0].rect_top.height

        self.state = np.array([bird_y, bird_vel, pipe_x, pipe_y], dtype=np.float32)
        self.done = False
        self.info = {}
        return self.state
    
    def step(self, action):
        """Executes one time step within the environment."""
        
        # Perform action: If action == 1, bird flaps
        if action == 1:
            self.game.bird.flap()

        # Update game state
        self.game.bird.update()
        self.game.background.move()

        # Move the pipes
        for pipe in self.game.pipes:
            pipe.move()

        # Check if we need to spawn new pipes
        self.game.pipe_timer += 1
        if self.game.pipe_timer > 100 / self.game.speed_factor:
            self.game.spawn_pipe()
            self.game.pipe_timer = 0

        # Update score if the bird passes a pipe
        self.game.update_score()

        # Remove pipes that have gone off screen
        self.game.pipes = [pipe for pipe in self.game.pipes if not pipe.is_off_screen()]

        # Check for collisions
        done = self.game.check_collision()

        # Calculate reward
        reward = 0
        if done:
            reward = -100  # Negative reward for game over
            self.done = True
        else:
            reward = 1  # Positive reward for each successful time step

        # Return the updated state
        bird_y = self.game.bird.rect.centery
        bird_vel = self.game.bird.velocity
        pipe_dist = self.game.pipes[0].rect_top.x - self.game.bird.rect.x if len(self.game.pipes) > 0 else config.SCREEN_WIDTH
        dist_to_ground = config.SCREEN_HEIGHT - bird_y
        dist_to_ceiling = bird_y

        self.state = np.array([bird_y, bird_vel, pipe_dist, dist_to_ground, dist_to_ceiling], dtype=np.float32)
        return self.state, reward, self.done, self.info
    
    def render(self, mode='human'):
        """Render the current state of the game"""
        if not self.render_enabled or self.done:
            return
        self.game.run()  # This will handle the rendering when enabled

    def close(self):
        """Clean up when closing the environment."""
        if self.game is not None:
            pygame.quit()  # Safely close Pygame
            

if __name__ == "__main__":
    env = FlyingBirdEnv(render=True)
    env.reset()
    for _ in range(1000):
        action = env.action_space.sample()  # Random action
        state, reward, done, info = env.step(action)
        env.render()
        time.sleep(0.2)
        if done:
            env.reset()
    env.close()