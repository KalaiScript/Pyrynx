"""
Typing Takedown — Particle System
Handles explosion effects, floating text, matrix rain, and ambient particles.
"""

import random
import math
import pygame
from settings import (
    PARTICLE_DESTROY, PARTICLE_DAMAGE, PARTICLE_COMBO, PARTICLE_MATRIX,
    SCREEN_WIDTH, SCREEN_HEIGHT, NEON_GREEN, NEON_CYAN, NEON_MAGENTA,
    NEON_YELLOW, TEXT_WHITE,
)


class Particle:
    """A single particle with physics and fading."""

    def __init__(self, x, y, vx, vy, color, lifetime, size=3, gravity=0.0, shrink=True):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.initial_size = size
        self.gravity = gravity
        self.shrink = shrink
        self.alive = True

    def update(self):
        """Update particle position and lifetime."""
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.lifetime -= 1
        if self.shrink:
            progress = self.lifetime / self.max_lifetime
            self.size = max(1, int(self.initial_size * progress))
        if self.lifetime <= 0:
            self.alive = False

    def draw(self, surface):
        """Draw the particle with alpha fade."""
        if not self.alive:
            return
        alpha = max(0, min(255, int(255 * (self.lifetime / self.max_lifetime))))
        r, g, b = self.color
        faded = (
            max(0, min(255, int(r * alpha / 255))),
            max(0, min(255, int(g * alpha / 255))),
            max(0, min(255, int(b * alpha / 255))),
        )
        if self.size <= 1:
            surface.set_at((int(self.x), int(self.y)), faded)
        else:
            pygame.draw.circle(surface, faded, (int(self.x), int(self.y)), self.size)


class FloatingText:
    """Floating score/combo text that rises and fades."""

    def __init__(self, text, x, y, color, font, duration=60):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font = font
        self.duration = duration
        self.max_duration = duration
        self.alive = True
        self.vy = -1.2

    def update(self):
        self.y += self.vy
        self.vy *= 0.98  # slow down
        self.duration -= 1
        if self.duration <= 0:
            self.alive = False

    def draw(self, surface):
        if not self.alive:
            return
        alpha = max(0, min(255, int(255 * (self.duration / self.max_duration))))
        r, g, b = self.color
        faded = (
            max(0, min(255, int(r * alpha / 255))),
            max(0, min(255, int(g * alpha / 255))),
            max(0, min(255, int(b * alpha / 255))),
        )
        text_surf = self.font.render(self.text, True, faded)
        rect = text_surf.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(text_surf, rect)


class MatrixRainDrop:
    """A single falling character for the matrix rain background."""

    def __init__(self):
        self.reset()
        # Start at random y for initial fill
        self.y = random.randint(-SCREEN_HEIGHT, SCREEN_HEIGHT)

    def reset(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(-200, -20)
        self.speed = random.uniform(1.0, 3.5)
        self.char = random.choice(
            "01{}[]():<>=+-*/&|!@#$%^~;ABCDEFabcdef0123456789"
        )
        self.color = random.choice(PARTICLE_MATRIX)
        self.alpha_factor = random.uniform(0.2, 0.6)
        self.change_timer = random.randint(5, 30)

    def update(self):
        self.y += self.speed
        self.change_timer -= 1
        if self.change_timer <= 0:
            self.char = random.choice(
                "01{}[]():<>=+-*/&|!@#$%^~;ABCDEFabcdef0123456789"
            )
            self.change_timer = random.randint(5, 30)
        if self.y > SCREEN_HEIGHT + 20:
            self.reset()

    def draw(self, surface, font):
        r, g, b = self.color
        faded = (
            int(r * self.alpha_factor),
            int(g * self.alpha_factor),
            int(b * self.alpha_factor),
        )
        char_surf = font.render(self.char, True, faded)
        surface.blit(char_surf, (self.x, int(self.y)))


class ParticleSystem:
    """Manages all particles, floating texts, and matrix rain."""

    def __init__(self):
        self.particles = []
        self.floating_texts = []
        self.matrix_rain = [MatrixRainDrop() for _ in range(80)]
        self.font_small = None  # Set after pygame.font.init()
        self.font_float = None

    def init_fonts(self, font_small, font_float):
        """Initialize fonts after pygame is ready."""
        self.font_small = font_small
        self.font_float = font_float

    def spawn_explosion(self, x, y, colors=None, count=20, speed=4.0):
        """Spawn a burst of particles at a position."""
        if colors is None:
            colors = PARTICLE_DESTROY
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            spd = random.uniform(1.0, speed)
            vx = math.cos(angle) * spd
            vy = math.sin(angle) * spd
            color = random.choice(colors)
            lifetime = random.randint(20, 50)
            size = random.randint(2, 5)
            self.particles.append(
                Particle(x, y, vx, vy, color, lifetime, size, gravity=0.05)
            )

    def spawn_damage_effect(self, x, y):
        """Red/magenta explosion when player takes damage."""
        self.spawn_explosion(x, y, colors=PARTICLE_DAMAGE, count=30, speed=5.0)

    def spawn_combo_effect(self, x, y):
        """Yellow/orange burst for combo milestones."""
        self.spawn_explosion(x, y, colors=PARTICLE_COMBO, count=25, speed=3.5)

    def spawn_correct_sparkle(self, x, y):
        """Small green sparkle for correct character."""
        for _ in range(5):
            angle = random.uniform(0, 2 * math.pi)
            spd = random.uniform(0.5, 2.0)
            vx = math.cos(angle) * spd
            vy = math.sin(angle) * spd
            self.particles.append(
                Particle(x, y, vx, vy, NEON_GREEN, random.randint(10, 25), 2, gravity=0.02)
            )

    def spawn_wrong_flash(self, x, y):
        """Small red flash for wrong character."""
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            spd = random.uniform(1.0, 3.0)
            vx = math.cos(angle) * spd
            vy = math.sin(angle) * spd
            self.particles.append(
                Particle(x, y, vx, vy, NEON_MAGENTA, random.randint(8, 18), 2, gravity=0.03)
            )

    def add_floating_text(self, text, x, y, color=NEON_GREEN, duration=60):
        """Add a floating score/text that rises and fades."""
        if self.font_float:
            self.floating_texts.append(
                FloatingText(text, x, y, color, self.font_float, duration)
            )

    def update(self):
        """Update all particles and floating texts."""
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.alive]

        for ft in self.floating_texts:
            ft.update()
        self.floating_texts = [ft for ft in self.floating_texts if ft.alive]

        for drop in self.matrix_rain:
            drop.update()

    def draw_matrix_rain(self, surface):
        """Draw matrix rain behind everything."""
        if self.font_small:
            for drop in self.matrix_rain:
                drop.draw(surface, self.font_small)

    def draw(self, surface):
        """Draw all particles and floating texts."""
        for p in self.particles:
            p.draw(surface)
        for ft in self.floating_texts:
            ft.draw(surface)

    def clear(self):
        """Clear all particles."""
        self.particles.clear()
        self.floating_texts.clear()
