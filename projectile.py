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
        self.x = float(start_x)
        self.y = float(start_y)
        self.target_x = float(target_x)
        self.target_y = float(target_y)
        self.color = color or NEON_GREEN
        self.speed = PROJECTILE_SPEED
        self.alive = True
        self.arrived = False

        dx = target_x - start_x
        dy = target_y - start_y
        dist = max(1.0, math.sqrt(dx * dx + dy * dy))
        self.vx = (dx / dist) * self.speed
        self.vy = (dy / dist) * self.speed

        self.trail = []
        self.trail_max = 8

    def update(self):
        if not self.alive:
            return
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.trail_max:
            self.trail.pop(0)
        self.x += self.vx
        self.y += self.vy
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        if math.sqrt(dx * dx + dy * dy) < self.speed * 2:
            self.arrived = True
            self.alive = False

    def draw(self, surface):
        if not self.alive and not self.trail:
            return
        for i, (tx, ty) in enumerate(self.trail):
            progress = i / max(1, len(self.trail))
            r, g, b = self.color
            tc = (int(r * progress * 0.5), int(g * progress * 0.5), int(b * progress * 0.5))
            size = max(1, int(PROJECTILE_WIDTH * progress))
            pygame.draw.circle(surface, tc, (int(tx), int(ty)), size)
        if self.alive:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), PROJECTILE_WIDTH + 1)
            glow_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*self.color, 60), (10, 10), 8)
            surface.blit(glow_surf, (int(self.x) - 10, int(self.y) - 10), special_flags=pygame.BLEND_ADD)
