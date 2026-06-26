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
    NEON_YELLOW, NEON_PURPLE, NEON_ORANGE,
    ENEMY_TYPE_NORMAL, ENEMY_TYPE_FAST, ENEMY_TYPE_ARMORED, ENEMY_TYPE_SPLITTER,
    ENEMY_TYPE_CONFIG,
)


class Enemy:
    """An enemy that the player must type to destroy."""

    def __init__(self, text: str, speed: float, is_boss: bool = False,
                 debug_display: str = None, enemy_type: str = ENEMY_TYPE_NORMAL):
        self.text = text                  # The correct text the player must type
        self.debug_display = debug_display  # Debug mode: broken code shown on screen
        self.typed = ""                   # Characters typed by the player so far
        self.is_boss = is_boss
        self.alive = True
        self.targeted = False             # True while the player is actively typing this enemy
        self.wrong_flash = 0              # Countdown frames for the red "wrong key" flash

        # ── Enemy type ────────────────────────────────────────────────────
        # Each type has its own speed multiplier, HP, border colour, and spawn weight.
        self.enemy_type = enemy_type
        type_cfg = ENEMY_TYPE_CONFIG.get(enemy_type, ENEMY_TYPE_CONFIG[ENEMY_TYPE_NORMAL])
        self.speed = speed * type_cfg["speed_mult"]          # final speed after type scaling
        self.hp    = ENEMY_BOSS_HP if is_boss else type_cfg["hp"]  # bosses always use BOSS_HP
        self.type_border_color = type_cfg["border_color"]    # None → uses default UI_BORDER

        # ── Dimensions ───────────────────────────────────────────────────
        # Width scales with text length; bosses get a taller box.
        self.text_width = max(ENEMY_WIDTH_MIN, len(self.display_text) * 11 + ENEMY_PADDING * 2)
        self.height     = ENEMY_HEIGHT + (10 if is_boss else 0)

        # ── Spawn position ────────────────────────────────────────────────
        # Random x within screen bounds, random y slightly above the top edge.
        margin = 40
        max_x  = SCREEN_WIDTH - self.text_width - margin
        self.x = random.randint(margin, max(margin + 1, max_x))
        self.y = ENEMY_SPAWN_Y - random.randint(0, 60)  # stagger entry timing

        # ── Visual state ─────────────────────────────────────────────────
        self.pulse_timer   = random.uniform(0, math.pi * 2)  # random phase so enemies look different
        self.entry_progress = 0.0   # 0.0 → 1.0 slide-in alpha animation

    @property
    def display_text(self) -> str:
        """The text shown to the player (may differ from answer in Debug mode)."""
        return self.debug_display if self.debug_display else self.text

    def update(self):
        """Move the enemy downward and advance visual timers."""
        self.y += self.speed
        self.pulse_timer    += 0.04    # drives border glow oscillation
        self.entry_progress = min(1.0, self.entry_progress + 0.03)  # fade in over ~33 frames

        if self.wrong_flash > 0:
            self.wrong_flash -= 1       # count down wrong-key flash frames

    def has_reached_player(self) -> bool:
        """Check if the enemy has reached the kill zone."""
        return self.y >= ENEMY_KILL_Y

    def check_input(self, char: str) -> bool:
        """
        Compare the next expected character against the player's keypress.
        On a match, appends the char to self.typed and returns True.
        On a miss, triggers a brief red flash and returns False.
        """
        if len(self.typed) >= len(self.text):
            return False  # already complete — shouldn't happen, safety guard
        expected = self.text[len(self.typed)]
        if char == expected:
            self.typed += char
            return True
        else:
            self.wrong_flash = 12   # flash for 12 frames (~0.2 s at 60 fps)
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
        """Draw the enemy as a floating code block with glow, progress bar, and type indicators."""
        # Fade in alpha: enemy slides into view over ~33 frames
        alpha = min(255, int(255 * self.entry_progress))

        # Background changes colour on wrong-key flash
        bg_color = BG_ENEMY_TARGETED if self.targeted else BG_ENEMY
        if self.wrong_flash > 0 and self.wrong_flash % 4 < 2:
            bg_color = (50, 10, 20)   # dark red blink

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
        elif self.type_border_color:
            # Typed enemy variant border
            glow_pulse = 0.7 + 0.3 * math.sin(self.pulse_timer * 2.5)
            tc = self.type_border_color
            border_col = (
                int(tc[0] * glow_pulse),
                int(tc[1] * glow_pulse),
                int(tc[2] * glow_pulse),
            )
            pygame.draw.rect(surface, border_col, rect, 2, border_radius=5)
        else:
            pygame.draw.rect(surface, UI_BORDER, rect, 1, border_radius=5)

        # ── Per-character text rendering ──────────────────────────────────
        # Colours: green = typed, bright cyan = next target char, dim = pending
        display   = self.display_text
        typed_len = len(self.typed)
        char_x = self.x + ENEMY_PADDING
        char_y = self.y + (self.height - font_code.get_height()) // 2

        for i, ch in enumerate(display):
            if i < typed_len:
                color = TEXT_CORRECT   # already typed correctly → green
            elif i == typed_len and self.targeted:
                color = NEON_CYAN      # next character to type → highlighted cyan
            else:
                color = TEXT_PENDING   # not yet reached → dim

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

        # Enemy type indicators
        if not self.is_boss and not self.debug_display and self.enemy_type != ENEMY_TYPE_NORMAL:
            type_labels = {
                ENEMY_TYPE_FAST: ("FAST", NEON_ORANGE),
                ENEMY_TYPE_ARMORED: ("ARMOR", (160, 160, 180)),
                ENEMY_TYPE_SPLITTER: ("SPLIT", NEON_GREEN),
            }
            label_info = type_labels.get(self.enemy_type)
            if label_info:
                lbl, col = label_info
                type_surf = font_small.render(lbl, True, col)
                surface.blit(type_surf, (self.x + ENEMY_PADDING, self.y - 16))

            # Armored: extra border thickness effect
            if self.enemy_type == ENEMY_TYPE_ARMORED and self.hp > 1:
                armor_rect = rect.inflate(-4, -4)
                pygame.draw.rect(surface, (100, 100, 120), armor_rect, 1, border_radius=4)

            # Fast: speed lines
            if self.enemy_type == ENEMY_TYPE_FAST:
                for i in range(3):
                    ly = self.y + 8 + i * 10
                    lx = self.x - 6 - i * 3
                    alpha_f = 0.3 + 0.2 * math.sin(self.pulse_timer * 5 + i)
                    line_col = (int(255 * alpha_f), int(140 * alpha_f), 0)
                    pygame.draw.line(surface, line_col, (lx, ly), (lx - 8, ly), 1)

            # Splitter: small split indicator dots
            if self.enemy_type == ENEMY_TYPE_SPLITTER:
                cx, cy = self.get_center()
                for dx_off in [-6, 6]:
                    pygame.draw.circle(surface, NEON_GREEN, (cx + dx_off, self.y - 8), 2)
