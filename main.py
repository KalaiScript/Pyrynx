"""
Typing Takedown — Main Entry Point
A Python typing combat game built with Pygame.

Defeat incoming enemies by typing Python code snippets,
terminal commands, and tech keywords!
"""

import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS
from game import Game


def main():
    """Initialize Pygame and launch the game."""
    pygame.init()
    pygame.display.set_caption(TITLE)

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Set window icon (terminal-style)
    icon = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.rect(icon, (0, 255, 136), (2, 2, 28, 28), border_radius=4)
    pygame.draw.rect(icon, (10, 10, 15), (4, 4, 24, 24), border_radius=3)
    pygame.draw.line(icon, (0, 255, 136), (8, 16), (14, 12), 2)
    pygame.draw.line(icon, (0, 255, 136), (8, 16), (14, 20), 2)
    pygame.draw.line(icon, (0, 229, 255), (16, 22), (24, 22), 2)
    pygame.display.set_icon(icon)

    # Run the game
    game = Game(screen)
    game.run()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
