from game import Game

if __name__ == '__main__':
    """Start the game by creating a Game object with rendering enabled"""
    game = Game(render=True)  # Enable rendering
    game.run()