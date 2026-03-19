#!/usr/bin/env python3
import sys
import os

# Add the current directory to the Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game import Game


def main():
    """Main function to start the Pacman game"""
    print("Starting Pacman Game...")
    print("Controls:")
    print("  - Arrow keys or WASD to move")
    print("  - Space to start from menu")
    print("  - R to restart after game over")
    print("  - Close window to quit")
    print("\nInitializing game...")
    
    # Create and run the game
    game = Game()
    game.run()

if __name__ == "__main__":
    main()