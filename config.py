# config.py
"""Configuration file for the flying bird game"""

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Bird settings
BIRD_START_X = 50    
BIRD_START_Y = 300   
BIRD_SCALE = (25, 25)  # Rescale bird to (width, height)

# Gravity settings
GRAVITY = 0.18       
FLAP_STRENGTH = -4.5

# Pipe settings
PIPE_WIDTH = 35
PIPE_HEIGHT = 400
PIPE_GAP = 220 
PIPE_VELOCITY = 2.7
PIPE_SCALE = (PIPE_WIDTH, PIPE_HEIGHT)  # Rescale pipes to fit screen

# Background settings
BACKGROUND_VELOCITY = 1.8
BACKGROUND_SCALE = (400, 600)  # Rescale background to fit screen

# Game settings
FPS = 60             

# Colors (RGB format)
COLOR_BLACK = (0, 0, 0)

# Paths to assets
BIRD_IMAGE_PATH = 'assets/images/bird.png'
PIPE_IMAGE_PATH = 'assets/images/pipe.png'
BACKGROUND_IMAGE_PATH = 'assets/images/background.png'
FLAP_SOUND_PATH = 'assets/sounds/flap.wav'
HIT_SOUND_PATH = 'assets/sounds/hit.wav'


FPS_TRAINING = 10  # Control the speed during training (for time.sleep)