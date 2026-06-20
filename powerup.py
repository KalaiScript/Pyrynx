"""
Typing Takedown — Power-Up System
Collectible power-ups that drop from defeated enemies.
"""

import pygame
import math
import random
from settings import (
    POWERUP_CONFIG, POWERUP_SPEED, POWERUP_SIZE, POWERUP_COLLECT_DIST,
    POWERUP_SHIELD, POWERUP_HEALTH, POWERUP_FREEZE, POWERUP_SCORE_BOOST, POWERUP_NUKE,
    ALL_POWERUPS, PLAYER_Y, SCREEN_HEIGHT, BG_PANEL,
)


class PowerUp:
    """A collectible power-up that falls from a defeated enemy's position."""

    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.powerup_type = powerup_type
        self.config = POWERUP_CONFIG[powerup_type]
        self.color = self.config["color"]
        self.label = self.config["label"]
        self.icon = self.config["icon"]
        self.speed = POWERUP_SPEED
        self.alive = True
        self.collected = False
        self.pulse_timer = random.uniform(0, math.pi * 2)
        self.size = POWERUP_SIZE

    def update(self):
        """Move the power-up downward."""
        self.y += self.speed
        self.pulse_timer += 0.08
        if self.y > SCREEN_HEIGHT + 30:
            self.alive = False

    def check_collect(self, player_x, player_y):
        """Check if the player is close enough to collect."""
        dx = self.x - player_x
        dy = self.y - player_y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < POWERUP_COLLECT_DIST:
            self.collected = True
            self.alive = False
            return True
        return False

    def draw(self, surface, font):
        """Draw the power-up with glowing effect."""
        if not self.alive:
            return

        pulse = 0.6 + 0.4 * math.sin(self.pulse_timer * 3)

        # Outer glow
        glow_size = int(self.size * 1.8)
        glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        glow_alpha = int(40 * pulse)
        pygame.draw.circle(
            glow_surf,
            (*self.color, glow_alpha),
            (glow_size, glow_size),
            glow_size,
        )
        surface.blit(
            glow_surf,
            (int(self.x) - glow_size, int(self.y) - glow_size),
            special_flags=pygame.BLEND_ADD,
        )

        # Inner circle
        r, g, b = self.color
        inner_color = (
            int(r * pulse),
            int(g * pulse),
            int(b * pulse),
        )
        pygame.draw.circle(surface, (15, 15, 25), (int(self.x), int(self.y)), self.size // 2 + 2)
        pygame.draw.circle(surface, inner_color, (int(self.x), int(self.y)), self.size // 2, 2)

        # Icon text
        icon_surf = font.render(self.icon, True, self.color)
        icon_rect = icon_surf.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(icon_surf, icon_rect)

        # Label below
        label_surf = font.render(self.label, True, self.color)
        label_rect = label_surf.get_rect(centerx=int(self.x), top=int(self.y) + self.size // 2 + 4)
        surface.blit(label_surf, label_rect)


def roll_powerup_drop(x, y):
    """
    Roll for a random power-up drop at the given position.
    Returns a PowerUp instance or None.
    """
    roll = random.random()
    cumulative = 0.0
    for ptype in ALL_POWERUPS:
        cumulative += POWERUP_CONFIG[ptype]["drop_rate"]
        if roll < cumulative:
            return PowerUp(x, y, ptype)
    return None
