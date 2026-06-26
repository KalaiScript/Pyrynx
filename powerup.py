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

        # Pull display / behaviour config from settings
        self.config = POWERUP_CONFIG[powerup_type]
        self.color  = self.config["color"]
        self.label  = self.config["label"]   # short text shown below the icon
        self.icon   = self.config["icon"]    # unicode symbol drawn in the centre

        self.speed     = POWERUP_SPEED       # fall speed (pixels per frame)
        self.alive     = True
        self.collected = False

        # Random phase offset so multiple power-ups pulse out of sync
        self.pulse_timer = random.uniform(0, math.pi * 2)
        self.size = POWERUP_SIZE             # radius used for drawing

    def update(self):
        """Move the power-up downward and advance the pulse animation."""
        self.y += self.speed
        self.pulse_timer += 0.08            # drives the glow oscillation

        # Despawn once it falls off screen (player missed it)
        if self.y > SCREEN_HEIGHT + 30:
            self.alive = False

    def check_collect(self, player_x, player_y):
        """
        Auto-collect if the player is within POWERUP_COLLECT_DIST pixels.
        Returns True when collected so the game loop can apply the effect.
        """
        dx = self.x - player_x
        dy = self.y - player_y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < POWERUP_COLLECT_DIST:
            self.collected = True
            self.alive = False
            return True
        return False

    def draw(self, surface, font):
        """Draw the power-up with a pulsing glow ring, icon, and label."""
        if not self.alive:
            return

        # pulse ranges 0.6 → 1.0 → 0.6, driving glow intensity and colour brightness
        pulse = 0.6 + 0.4 * math.sin(self.pulse_timer * 3)

        # ── Outer additive glow ring ──────────────────────────────────────
        glow_size  = int(self.size * 1.8)
        glow_surf  = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        glow_alpha = int(40 * pulse)
        pygame.draw.circle(
            glow_surf,
            (*self.color, glow_alpha),
            (glow_size, glow_size),
            glow_size,
        )
        # BLEND_ADD makes the glow brighten whatever is behind it
        surface.blit(
            glow_surf,
            (int(self.x) - glow_size, int(self.y) - glow_size),
            special_flags=pygame.BLEND_ADD,
        )

        # ── Inner solid circle ────────────────────────────────────────────
        r, g, b = self.color
        # Scale colour with pulse so the circle "breathes"
        inner_color = (
            int(r * pulse),
            int(g * pulse),
            int(b * pulse),
        )
        # Dark filled background circle, then a coloured ring on top
        pygame.draw.circle(surface, (15, 15, 25), (int(self.x), int(self.y)), self.size // 2 + 2)
        pygame.draw.circle(surface, inner_color, (int(self.x), int(self.y)), self.size // 2, 2)

        # ── Icon ─────────────────────────────────────────────────────────
        icon_surf = font.render(self.icon, True, self.color)
        icon_rect = icon_surf.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(icon_surf, icon_rect)

        # ── Label below ──────────────────────────────────────────────────
        label_surf = font.render(self.label, True, self.color)
        label_rect = label_surf.get_rect(centerx=int(self.x), top=int(self.y) + self.size // 2 + 4)
        surface.blit(label_surf, label_rect)


def roll_powerup_drop(x, y):
    """
    Roll a weighted random check for a power-up drop at position (x, y).

    Each power-up type has a 'drop_rate' between 0.0 and 1.0 in settings.
    We iterate through ALL_POWERUPS in order, accumulating the cumulative
    probability until the random roll is exceeded — then that type drops.
    Returns a PowerUp instance, or None if the roll misses all thresholds
    (i.e. the enemy drops nothing this time).
    """
    roll       = random.random()   # single random value in [0, 1)
    cumulative = 0.0

    for ptype in ALL_POWERUPS:
        cumulative += POWERUP_CONFIG[ptype]["drop_rate"]
        if roll < cumulative:
            return PowerUp(x, y, ptype)  # this type wins the roll

    return None  # roll exceeded all thresholds — no drop
