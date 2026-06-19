"""
Typing Takedown — Enemy Class
Enemies that carry code text and move toward the player.
"""

import pygame
import math
import random
from settings import (
    SCREEN_WIDTH, ENEMY_SPAWN_Y, ENEMY_KILL_Y, ENEMY_PADDING,
    ENEMY_HEIGHT, ENEMY_WIDTH_MIN, ENEMY_BOSS_HP,
    BG_ENEMY, BG_ENEMY_TARGETED, NEON_GREEN, NEON_CYAN, NEON_MAGENTA,
    TEXT_CORRECT, TEXT_PENDING, TEXT_WRONG, UI_BORDER, UI_BORDER_GLOW,
    NEON_YELLOW, NEON_PURPLE,
)


class Enemy:
    """An enemy that the player must type to destroy."""

    def __init__(self, text: str, speed: float, is_boss: bool = False,
                 debug_display: str = None):
        self.text = text                  # The text the player must type
        self.debug_display = debug_display  # For Debug mode: broken code shown
        self.typed = ""                   # What the player has typed so far
        self.speed = speed
        self.is_boss = is_boss
        self.hp = ENEMY_BOSS_HP if is_boss else 1
        self.alive = True
        self.targeted = False             # Is the player currently typing this enemy?
        self.wrong_flash = 0              # Frames of wrong-character flash

        # Calculate width based on text length
        self.text_width = max(ENEMY_WIDTH_MIN, len(self.display_text) * 11 + ENEMY_PADDING * 2)
        self.height = ENEMY_HEIGHT + (10 if is_boss else 0)

        # Position: random x, start above screen
        margin = 40
        max_x = SCREEN_WIDTH - self.text_width - margin
        self.x = random.randint(margin, max(margin + 1, max_x))
        self.y = ENEMY_SPAWN_Y - random.randint(0, 60)

        # Visual
        self.pulse_timer = random.uniform(0, math.pi * 2)
        self.entry_progress = 0.0  # for slide-in animation

    @property
    def display_text(self) -> str:
        """The text shown to the player (may differ from answer in Debug mode)."""
        return self.debug_display if self.debug_display else self.text

    def update(self):
        """Move the enemy downward."""
        self.y += self.speed
        self.pulse_timer += 0.04
        self.entry_progress = min(1.0, self.entry_progress + 0.03)

        if self.wrong_flash > 0:
            self.wrong_flash -= 1

    def has_reached_player(self) -> bool:
        """Check if the enemy has reached the kill zone."""
        return self.y >= ENEMY_KILL_Y

    def check_input(self, char: str) -> bool:
        """
        Check if the next expected character matches.
        Returns True for correct, False for wrong.
        """
        if len(self.typed) >= len(self.text):
            return False
        expected = self.text[len(self.typed)]
        if char == expected:
            self.typed += char
            return True
        else:
            self.wrong_flash = 12
            return False

    def is_complete(self) -> bool:
        """Check if the full text has been typed."""
        return self.typed == self.text

    def matches_start(self, char: str) -> bool:
        """Check if this enemy's text starts with the given character."""
        return len(self.text) > 0 and self.text[0] == char and len(self.typed) == 0

    def get_progress(self) -> float:
        """Get typing progress as 0.0 to 1.0."""
        if len(self.text) == 0:
            return 1.0
        return len(self.typed) / len(self.text)

    def get_center(self) -> tuple:
        """Get the center position of the enemy."""
        return (
            self.x + self.text_width // 2,
            self.y + self.height // 2,
        )

    def draw(self, surface, font_code, font_small):
        """Draw the enemy as a floating code block."""
        # Slide-in alpha
        alpha = min(255, int(255 * self.entry_progress))

        # Background
        bg_color = BG_ENEMY_TARGETED if self.targeted else BG_ENEMY
        if self.wrong_flash > 0 and self.wrong_flash % 4 < 2:
            bg_color = (50, 10, 20)

        rect = pygame.Rect(self.x, int(self.y), self.text_width, self.height)

        # Draw panel background
        pygame.draw.rect(surface, bg_color, rect, border_radius=5)

        # Border with glow for targeted/boss
        if self.targeted:
            glow_pulse = 0.6 + 0.4 * math.sin(self.pulse_timer * 3)
            border_col = (
                int(NEON_CYAN[0] * glow_pulse),
                int(NEON_CYAN[1] * glow_pulse),
                int(NEON_CYAN[2] * glow_pulse),
            )
            pygame.draw.rect(surface, border_col, rect, 2, border_radius=5)

            # Outer glow
            glow_rect = rect.inflate(6, 6)
            glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(
                glow_surf,
                (*NEON_CYAN, int(25 * glow_pulse)),
                (0, 0, glow_rect.width, glow_rect.height),
                border_radius=7,
            )
            surface.blit(glow_surf, glow_rect.topleft)
        elif self.is_boss:
            glow_pulse = 0.6 + 0.4 * math.sin(self.pulse_timer * 2)
            border_col = (
                int(NEON_PURPLE[0] * glow_pulse),
                int(NEON_PURPLE[1] * glow_pulse),
                int(NEON_PURPLE[2] * glow_pulse),
            )
            pygame.draw.rect(surface, border_col, rect, 2, border_radius=5)
        else:
            pygame.draw.rect(surface, UI_BORDER, rect, 1, border_radius=5)

        # Draw text character-by-character with coloring
        display = self.display_text
        typed_len = len(self.typed)
        char_x = self.x + ENEMY_PADDING
        char_y = self.y + (self.height - font_code.get_height()) // 2

        for i, ch in enumerate(display):
            if i < typed_len:
                # Already typed correctly
                color = TEXT_CORRECT
            elif i == typed_len and self.targeted:
                # Next character to type (highlighted)
                color = NEON_CYAN
            else:
                # Not yet typed
                color = TEXT_PENDING

            char_surf = font_code.render(ch, True, color)
            surface.blit(char_surf, (char_x, char_y))
            char_x += char_surf.get_width()

        # Progress bar under the text block
        if typed_len > 0:
            progress = self.get_progress()
            bar_y = self.y + self.height - 3
            bar_width = int((self.text_width - 8) * progress)
            bar_color = NEON_GREEN if not self.is_boss else NEON_PURPLE
            pygame.draw.rect(
                surface, bar_color,
                (self.x + 4, bar_y, bar_width, 2),
                border_radius=1,
            )

        # Boss indicator
        if self.is_boss:
            boss_label = font_small.render("BOSS", True, NEON_PURPLE)
            surface.blit(boss_label, (self.x + ENEMY_PADDING, self.y - 16))

            # HP pips for boss
            pip_x = self.x + ENEMY_PADDING + 50
            for i in range(self.hp):
                pygame.draw.circle(
                    surface, NEON_PURPLE,
                    (pip_x + i * 14, self.y - 10),
                    4,
                )

        # Debug mode: show "FIX:" label
        if self.debug_display:
            fix_label = font_small.render("FIX →", True, NEON_YELLOW)
            surface.blit(fix_label, (self.x + ENEMY_PADDING, self.y - 16))
