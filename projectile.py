"""
Typing Takedown — Projectile / Attack Effects
Visual projectile that fires from the player toward a defeated enemy.
"""

import pygame
import math
from settings import NEON_GREEN, PROJECTILE_SPEED, PROJECTILE_WIDTH


class Projectile:
    """An energy bolt fired from the player to a destroyed enemy."""

    def __init__(self, start_x, start_y, target_x, target_y, color=None):
        # Current position (float for sub-pixel precision)
        self.x = float(start_x)
        self.y = float(start_y)

        # Destination — used to detect arrival
        self.target_x = float(target_x)
        self.target_y = float(target_y)

        self.color = color or NEON_GREEN
        self.speed = PROJECTILE_SPEED
        self.alive   = True    # actively moving
        self.arrived = False   # reached target (trail may still be visible)

        # ── Velocity ─────────────────────────────────────────────────────
        # Normalise the direction vector so the bolt moves at a constant speed
        # regardless of how far away the target is.
        dx   = target_x - start_x
        dy   = target_y - start_y
        dist = max(1.0, math.sqrt(dx * dx + dy * dy))  # clamp to avoid /0
        self.vx = (dx / dist) * self.speed
        self.vy = (dy / dist) * self.speed

        # ── Trail (ring buffer) ──────────────────────────────────────────
        # Stores the last N positions so we can draw a fading tail.
        self.trail     = []
        self.trail_max = 8   # keep up to 8 past positions

    def update(self):
        """Advance position toward target and record trail history."""
        if not self.alive:
            return

        # Save current position before moving (oldest entries popped from front)
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.trail_max:
            self.trail.pop(0)

        # Move
        self.x += self.vx
        self.y += self.vy

        # Check arrival: within 2× speed distance of the target → snap complete
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        if math.sqrt(dx * dx + dy * dy) < self.speed * 2:
            self.arrived = True
            self.alive   = False  # stop moving; trail will fade naturally

    def draw(self, surface):
        """
        Draw the fading trail and the live bolt head.
        The trail draws older positions dimmer and smaller — giving a
        motion-blur / comet tail effect without any extra surfaces.
        """
        if not self.alive and not self.trail:
            return  # nothing left to draw

        # ── Fading trail dots ─────────────────────────────────────────────
        for i, (tx, ty) in enumerate(self.trail):
            # progress goes from 0.0 (oldest) to ~1.0 (newest) — scales brightness
            progress = i / max(1, len(self.trail))
            r, g, b  = self.color
            # Dim older trail dots by scaling the colour down
            tc   = (int(r * progress * 0.5), int(g * progress * 0.5), int(b * progress * 0.5))
            size = max(1, int(PROJECTILE_WIDTH * progress))
            pygame.draw.circle(surface, tc, (int(tx), int(ty)), size)

        # ── Live bolt head ────────────────────────────────────────────────
        if self.alive:
            # Solid core
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), PROJECTILE_WIDTH + 1)

            # Small additive glow halo around the head
            glow_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*self.color, 60), (10, 10), 8)
            surface.blit(glow_surf, (int(self.x) - 10, int(self.y) - 10), special_flags=pygame.BLEND_ADD)
