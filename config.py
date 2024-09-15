# config.py
"""Configuration file for the flying bird game"""

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Bird settings
BIRD_START_X = 50    
BIRD_START_Y = 300   
BIRD_SCALE = (50, 35)  # Rescale bird to (width, height)

# Gravity settings
GRAVITY = 0.20       
FLAP_STRENGTH = -5 

# Pipe settings
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 150       
PIPE_VELOCITY = 4    
PIPE_SCALE = (60, 500)  # Rescale pipes to fit screen

# Background settings
BACKGROUND_VELOCITY = 2
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