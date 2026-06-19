"""
Typing Takedown — Player Class
Manages health, position, rendering, and damage effects for the player.
"""

import pygame
import math
from settings import (
    PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT,
    NEON_GREEN, NEON_CYAN, NEON_MAGENTA, BG_PANEL, TEXT_WHITE,
    UI_BORDER, SCREEN_WIDTH,
)


class Player:
    """The player character — a glowing terminal at the bottom of the screen."""

    def __init__(self, max_health: int = 5):
        self.x = PLAYER_X
        self.y = PLAYER_Y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.max_health = max_health
        self.health = max_health
        self.alive = True

        # Visual state
        self.pulse_timer = 0.0
        self.damage_flash = 0     # frames of red flash remaining
        self.shield_active = False

    def reset(self, max_health: int = 5):
        """Reset player state for a new game."""
        self.max_health = max_health
        self.health = max_health
        self.alive = True
        self.damage_flash = 0
        self.shield_active = False

    def take_damage(self, amount: int = 1):
        """Reduce health and trigger damage flash."""
        if self.shield_active:
            self.shield_active = False
            return False  # damage blocked

        self.health -= amount
        self.damage_flash = 20  # flash for 20 frames
        if self.health <= 0:
            self.health = 0
            self.alive = False
        return True  # damage applied

    def heal(self, amount: int = 1):
        """Restore health up to max."""
        self.health = min(self.health + amount, self.max_health)

    def update(self):
        """Update visual effects."""
        self.pulse_timer += 0.05
        if self.damage_flash > 0:
            self.damage_flash -= 1

    def draw(self, surface):
        """Draw the player as a glowing terminal/monitor."""
        cx = self.x
        cy = self.y

        # Pulsing glow intensity
        glow = 0.5 + 0.5 * math.sin(self.pulse_timer)

        # Determine color based on state
        if self.damage_flash > 0 and self.damage_flash % 4 < 2:
            border_color = NEON_MAGENTA
            body_color = (40, 10, 20)
        else:
            base_g = int(NEON_CYAN[1] * (0.6 + 0.4 * glow))
            border_color = (0, base_g, NEON_CYAN[2])
            body_color = BG_PANEL

        # Terminal body
        body_rect = pygame.Rect(
            cx - self.width // 2,
            cy - self.height // 2,
            self.width,
            self.height,
        )
        pygame.draw.rect(surface, body_color, body_rect, border_radius=6)
        pygame.draw.rect(surface, border_color, body_rect, 2, border_radius=6)

        # Screen area inside terminal
        screen_rect = pygame.Rect(
            cx - self.width // 2 + 6,
            cy - self.height // 2 + 6,
            self.width - 12,
            self.height - 12,
        )
        screen_color = (8, 12, 20)
        pygame.draw.rect(surface, screen_color, screen_rect, border_radius=3)

        # Blinking cursor inside the terminal screen
        if int(self.pulse_timer * 2) % 2 == 0:
            cursor_x = cx - self.width // 2 + 14
            cursor_y = cy - 6
            pygame.draw.rect(surface, NEON_GREEN, (cursor_x, cursor_y, 10, 14))

        # Terminal stand
        stand_x = cx - 8
        stand_y = cy + self.height // 2
        pygame.draw.rect(surface, UI_BORDER, (stand_x, stand_y, 16, 8))
        pygame.draw.rect(surface, UI_BORDER, (stand_x - 10, stand_y + 8, 36, 4), border_radius=2)

        # Glow effect (faint circle behind terminal)
        glow_surf = pygame.Surface((200, 100), pygame.SRCALPHA)
        glow_alpha = int(30 * glow)
        pygame.draw.ellipse(
            glow_surf,
            (*border_color, glow_alpha),
            (0, 0, 200, 100),
        )
        surface.blit(
            glow_surf,
            (cx - 100, cy - 50),
            special_flags=pygame.BLEND_ADD,
        )

        # Shield visual
        if self.shield_active:
            shield_surf = pygame.Surface((self.width + 30, self.height + 30), pygame.SRCALPHA)
            pygame.draw.ellipse(
                shield_surf,
                (0, 229, 255, 50),
                (0, 0, self.width + 30, self.height + 30),
            )
            pygame.draw.ellipse(
                shield_surf,
                (0, 229, 255, 120),
                (0, 0, self.width + 30, self.height + 30),
                2,
            )
            surface.blit(
                shield_surf,
                (cx - (self.width + 30) // 2, cy - (self.height + 30) // 2),
            )

    def get_center(self) -> tuple:
        """Get player center position."""
        return (self.x, self.y)
