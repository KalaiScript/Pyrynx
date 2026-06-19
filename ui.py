"""
Typing Takedown — UI System
All menu screens, HUD, game over, pause overlays, and visual effects.
"""

import pygame
import math
import time
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BG_DARK, BG_PANEL, BG_PANEL_HOVER,
    NEON_GREEN, NEON_CYAN, NEON_MAGENTA, NEON_YELLOW, NEON_PURPLE, NEON_ORANGE,
    TEXT_WHITE, TEXT_DIM, TEXT_CORRECT, TEXT_WRONG, TEXT_CURSOR,
    UI_HEALTH_FULL, UI_HEALTH_MID, UI_HEALTH_LOW, UI_BORDER,
    SCANLINE_ALPHA, SCANLINE_GAP,
    STATE_MENU, STATE_MODE_SELECT, STATE_DIFFICULTY_SELECT,
    STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER, STATE_HIGH_SCORES,
    ALL_MODES, MODE_DESCRIPTIONS, ALL_DIFFICULTIES,
    FONT_MONO, FONT_MONO_FALLBACK, FONT_SANS, FONT_SANS_FALLBACK,
)


class UI:
    """Handles all game UI rendering."""

    def __init__(self):
        self.fonts = {}
        self.scanline_surface = None
        self.title_timer = 0.0
        self.cursor_blink = 0.0

    def init(self):
        """Initialize fonts and pre-rendered surfaces."""
        # Try preferred fonts, fall back to system defaults
        mono = FONT_MONO
        try:
            test = pygame.font.SysFont(mono, 20)
            if test.size("A")[0] == 0:
                mono = FONT_MONO_FALLBACK
        except Exception:
            mono = FONT_MONO_FALLBACK

        sans = FONT_SANS
        try:
            test = pygame.font.SysFont(sans, 20)
            if test.size("A")[0] == 0:
                sans = FONT_SANS_FALLBACK
        except Exception:
            sans = FONT_SANS_FALLBACK

        self.fonts = {
            "title": pygame.font.SysFont(mono, 52, bold=True),
            "subtitle": pygame.font.SysFont(mono, 22),
            "menu": pygame.font.SysFont(sans, 28),
            "menu_small": pygame.font.SysFont(sans, 18),
            "hud": pygame.font.SysFont(mono, 20),
            "hud_large": pygame.font.SysFont(mono, 28, bold=True),
            "code": pygame.font.SysFont(mono, 18),
            "code_large": pygame.font.SysFont(mono, 22),
            "small": pygame.font.SysFont(mono, 14),
            "float": pygame.font.SysFont(mono, 16, bold=True),
            "result_title": pygame.font.SysFont(mono, 36, bold=True),
            "result": pygame.font.SysFont(mono, 22),
            "result_small": pygame.font.SysFont(mono, 16),
        }

        # Pre-render scanline overlay
        self.scanline_surface = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
        )
        for y in range(0, SCREEN_HEIGHT, SCANLINE_GAP):
            pygame.draw.line(
                self.scanline_surface,
                (0, 0, 0, SCANLINE_ALPHA),
                (0, y), (SCREEN_WIDTH, y),
            )

    def get_font(self, name):
        return self.fonts.get(name, self.fonts["menu"])

    def draw_scanlines(self, surface):
        """Draw CRT scanline overlay."""
        if self.scanline_surface:
            surface.blit(self.scanline_surface, (0, 0))

    # ── Main Menu ─────────────────────────────────────────────────────────

    def draw_menu(self, surface, selected_index, menu_items):
        """Draw the main menu screen."""
        self.title_timer += 0.02
        self.cursor_blink += 0.05

        # Title
        title_font = self.fonts["title"]
        title_text = "TYPING TAKEDOWN"

        # Glitch effect on title
        title_y = 140
        for i, ch in enumerate(title_text):
            offset_y = int(math.sin(self.title_timer * 3 + i * 0.5) * 2)
            hue_shift = (math.sin(self.title_timer + i * 0.3) + 1) / 2
            r = int(NEON_GREEN[0] + (NEON_CYAN[0] - NEON_GREEN[0]) * hue_shift)
            g = int(NEON_GREEN[1] + (NEON_CYAN[1] - NEON_GREEN[1]) * hue_shift)
            b = int(NEON_GREEN[2] + (NEON_CYAN[2] - NEON_GREEN[2]) * hue_shift)
            char_surf = title_font.render(ch, True, (r, g, b))
            x = SCREEN_WIDTH // 2 - title_font.size(title_text)[0] // 2
            x += title_font.size(title_text[:i])[0]
            surface.blit(char_surf, (x, title_y + offset_y))

        # Subtitle
        sub = self.fonts["subtitle"]
        sub_text = "// Python Syntax Battle Game"
        sub_surf = sub.render(sub_text, True, TEXT_DIM)
        sub_rect = sub_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=200)
        surface.blit(sub_surf, sub_rect)

        # Menu items
        menu_y = 300
        for i, item in enumerate(menu_items):
            is_selected = (i == selected_index)
            color = NEON_CYAN if is_selected else TEXT_DIM
            font = self.fonts["menu"]

            prefix = "> " if is_selected else "  "
            text = prefix + item

            text_surf = font.render(text, True, color)
            text_rect = text_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=menu_y + i * 50)

            # Selection highlight bar
            if is_selected:
                bar_rect = pygame.Rect(
                    SCREEN_WIDTH // 2 - 180,
                    menu_y + i * 50 - 5,
                    360, 40,
                )
                pygame.draw.rect(surface, BG_PANEL_HOVER, bar_rect, border_radius=5)
                pygame.draw.rect(surface, NEON_CYAN, bar_rect, 1, border_radius=5)

            surface.blit(text_surf, text_rect)

        # Footer
        footer = self.fonts["small"]
        ft = footer.render("↑/↓ Navigate   ENTER Select   ESC Quit", True, TEXT_DIM)
        surface.blit(ft, ft.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 30))

    # ── Mode Select ───────────────────────────────────────────────────────

    def draw_mode_select(self, surface, selected_index):
        """Draw the mode selection screen."""
        # Header
        header = self.fonts["result_title"]
        h_surf = header.render("SELECT MODE", True, NEON_CYAN)
        surface.blit(h_surf, h_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=60))

        # Mode list
        mode_y = 150
        mode_colors = [NEON_GREEN, NEON_CYAN, NEON_PURPLE, NEON_YELLOW, NEON_ORANGE, NEON_MAGENTA]
        for i, mode in enumerate(ALL_MODES):
            is_selected = (i == selected_index)
            color = mode_colors[i % len(mode_colors)] if is_selected else TEXT_DIM
            font = self.fonts["menu"]
            small = self.fonts["menu_small"]

            prefix = "> " if is_selected else "  "
            text_surf = font.render(prefix + mode, True, color)

            y = mode_y + i * 70
            text_rect = text_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=y)

            if is_selected:
                bar = pygame.Rect(SCREEN_WIDTH // 2 - 250, y - 5, 500, 55)
                pygame.draw.rect(surface, BG_PANEL_HOVER, bar, border_radius=5)
                pygame.draw.rect(surface, color, bar, 1, border_radius=5)

                # Description
                desc = MODE_DESCRIPTIONS.get(mode, "")
                desc_surf = small.render(desc, True, TEXT_DIM)
                desc_rect = desc_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=y + 30)
                surface.blit(desc_surf, desc_rect)

            surface.blit(text_surf, text_rect)

        # Footer
        footer = self.fonts["small"]
        ft = footer.render("↑/↓ Navigate   ENTER Select   ESC Back", True, TEXT_DIM)
        surface.blit(ft, ft.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 30))

    # ── Difficulty Select ─────────────────────────────────────────────────

    def draw_difficulty_select(self, surface, selected_index):
        """Draw difficulty selection screen."""
        header = self.fonts["result_title"]
        h_surf = header.render("SELECT DIFFICULTY", True, NEON_YELLOW)
        surface.blit(h_surf, h_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=100))

        diff_colors = [NEON_GREEN, NEON_YELLOW, NEON_MAGENTA]
        diff_descs = [
            "Slower enemies, simpler words, more health",
            "Balanced speed and complexity",
            "Fast enemies, complex code, minimal health",
        ]

        diff_y = 260
        for i, diff in enumerate(ALL_DIFFICULTIES):
            is_selected = (i == selected_index)
            color = diff_colors[i] if is_selected else TEXT_DIM
            font = self.fonts["menu"]

            prefix = "> " if is_selected else "  "
            text_surf = font.render(prefix + diff, True, color)
            y = diff_y + i * 90
            text_rect = text_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=y)

            if is_selected:
                bar = pygame.Rect(SCREEN_WIDTH // 2 - 220, y - 5, 440, 70)
                pygame.draw.rect(surface, BG_PANEL_HOVER, bar, border_radius=5)
                pygame.draw.rect(surface, color, bar, 1, border_radius=5)
                desc_surf = self.fonts["menu_small"].render(diff_descs[i], True, TEXT_DIM)
                surface.blit(desc_surf, desc_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=y + 35))

            surface.blit(text_surf, text_rect)

        footer = self.fonts["small"]
        ft = footer.render("↑/↓ Navigate   ENTER Select   ESC Back", True, TEXT_DIM)
        surface.blit(ft, ft.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 30))

    # ── In-Game HUD ───────────────────────────────────────────────────────

    def draw_hud(self, surface, player, stats, mode, time_left=None):
        """Draw the in-game heads-up display."""
        font = self.fonts["hud"]
        font_large = self.fonts["hud_large"]
        small = self.fonts["small"]

        # ── Top-left: Score + Combo ──
        score_text = f"SCORE: {stats.score:,}"
        score_surf = font_large.render(score_text, True, NEON_GREEN)
        surface.blit(score_surf, (20, 15))

        if stats.combo > 1:
            combo_text = f"COMBO x{stats.multiplier}  ({stats.combo} streak)"
            combo_surf = font.render(combo_text, True, NEON_YELLOW)
            surface.blit(combo_surf, (20, 48))

        # ── Top-right: WPM + Accuracy ──
        wpm_text = f"WPM: {stats.get_wpm():.0f}"
        acc_text = f"ACC: {stats.get_accuracy():.1f}%"
        wpm_surf = font.render(wpm_text, True, NEON_CYAN)
        acc_surf = font.render(acc_text, True, NEON_CYAN)
        surface.blit(wpm_surf, (SCREEN_WIDTH - wpm_surf.get_width() - 20, 15))
        surface.blit(acc_surf, (SCREEN_WIDTH - acc_surf.get_width() - 20, 40))

        # ── Top-center: Timer (Time Attack mode) ──
        if time_left is not None:
            mins = int(time_left) // 60
            secs = int(time_left) % 60
            timer_color = NEON_MAGENTA if time_left < 10 else NEON_CYAN
            timer_text = f"{mins}:{secs:02d}"
            timer_surf = font_large.render(timer_text, True, timer_color)
            surface.blit(timer_surf, timer_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=12))

        # ── Top-center: Mode label ──
        mode_surf = small.render(mode, True, TEXT_DIM)
        surface.blit(mode_surf, mode_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=45))

        # ── Bottom-left: Health Bar ──
        self._draw_health_bar(surface, player, 20, SCREEN_HEIGHT - 40)

        # ── Bottom: Enemies defeated ──
        ed_text = f"Defeated: {stats.enemies_defeated}"
        ed_surf = small.render(ed_text, True, TEXT_DIM)
        surface.blit(ed_surf, (SCREEN_WIDTH - ed_surf.get_width() - 20, SCREEN_HEIGHT - 35))

    def _draw_health_bar(self, surface, player, x, y):
        """Draw segmented health bar."""
        seg_width = 24
        seg_height = 16
        gap = 3
        total_w = player.max_health * (seg_width + gap) - gap

        for i in range(player.max_health):
            sx = x + i * (seg_width + gap)
            if i < player.health:
                ratio = player.health / player.max_health
                if ratio > 0.6:
                    color = UI_HEALTH_FULL
                elif ratio > 0.3:
                    color = UI_HEALTH_MID
                else:
                    color = UI_HEALTH_LOW
                pygame.draw.rect(surface, color, (sx, y, seg_width, seg_height), border_radius=3)
            else:
                pygame.draw.rect(surface, (30, 30, 40), (sx, y, seg_width, seg_height), border_radius=3)
                pygame.draw.rect(surface, UI_BORDER, (sx, y, seg_width, seg_height), 1, border_radius=3)

        # HP label
        hp_surf = self.fonts["small"].render(f"HP {player.health}/{player.max_health}", True, TEXT_DIM)
        surface.blit(hp_surf, (x + total_w + 10, y + 1))

    # ── Input Display ─────────────────────────────────────────────────────

    def draw_input_display(self, surface, current_input, targeted_enemy):
        """Draw the current typing input at the bottom of the screen."""
        self.cursor_blink += 0.06
        font = self.fonts["code_large"]

        # Input box background
        box_w = 500
        box_h = 40
        box_x = SCREEN_WIDTH // 2 - box_w // 2
        box_y = SCREEN_HEIGHT - 75

        pygame.draw.rect(surface, BG_PANEL, (box_x, box_y, box_w, box_h), border_radius=5)
        border_col = NEON_CYAN if targeted_enemy else UI_BORDER
        pygame.draw.rect(surface, border_col, (box_x, box_y, box_w, box_h), 1, border_radius=5)

        # Prompt
        prompt = "> "
        prompt_surf = font.render(prompt, True, NEON_GREEN)
        surface.blit(prompt_surf, (box_x + 10, box_y + 8))

        # Current input text
        text_x = box_x + 10 + prompt_surf.get_width()
        if current_input:
            input_surf = font.render(current_input, True, TEXT_WHITE)
            surface.blit(input_surf, (text_x, box_y + 8))
            text_x += input_surf.get_width()

        # Blinking cursor
        if int(self.cursor_blink) % 2 == 0:
            cursor_rect = pygame.Rect(text_x + 2, box_y + 8, 2, font.get_height())
            pygame.draw.rect(surface, TEXT_CURSOR, cursor_rect)

    # ── Pause Screen ──────────────────────────────────────────────────────

    def draw_pause(self, surface, selected_index):
        """Draw pause overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        # Title
        title = self.fonts["result_title"]
        t_surf = title.render("PAUSED", True, NEON_CYAN)
        surface.blit(t_surf, t_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=220))

        # Options
        items = ["Resume", "Restart", "Main Menu"]
        for i, item in enumerate(items):
            is_sel = (i == selected_index)
            color = NEON_CYAN if is_sel else TEXT_DIM
            prefix = "> " if is_sel else "  "
            surf = self.fonts["menu"].render(prefix + item, True, color)
            rect = surf.get_rect(centerx=SCREEN_WIDTH // 2, top=310 + i * 50)
            surface.blit(surf, rect)

        footer = self.fonts["small"]
        ft = footer.render("ESC Resume   ↑/↓ Navigate   ENTER Select", True, TEXT_DIM)
        surface.blit(ft, ft.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 30))

    # ── Game Over Screen ──────────────────────────────────────────────────

    def draw_game_over(self, surface, stats_summary, mode, is_new_high, selected_index):
        """Draw the game over results screen."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Title
        title = self.fonts["result_title"]
        t_surf = title.render("GAME OVER", True, NEON_MAGENTA)
        surface.blit(t_surf, t_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=60))

        if is_new_high:
            nh_surf = self.fonts["subtitle"].render("★ NEW HIGH SCORE! ★", True, NEON_YELLOW)
            surface.blit(nh_surf, nh_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=105))

        # Stats panel
        panel_x = SCREEN_WIDTH // 2 - 250
        panel_y = 145
        panel_w = 500
        panel_h = 320
        pygame.draw.rect(surface, BG_PANEL, (panel_x, panel_y, panel_w, panel_h), border_radius=8)
        pygame.draw.rect(surface, UI_BORDER, (panel_x, panel_y, panel_w, panel_h), 1, border_radius=8)

        font = self.fonts["result"]
        small = self.fonts["result_small"]

        s = stats_summary
        stats_lines = [
            ("Score", f"{s['score']:,}", NEON_GREEN),
            ("WPM", f"{s['wpm']:.1f}", NEON_CYAN),
            ("Accuracy", f"{s['accuracy']:.1f}%", NEON_CYAN),
            ("Max Combo", f"x{s['max_combo']}", NEON_YELLOW),
            ("Enemies Defeated", str(s['enemies_defeated']), TEXT_WHITE),
            ("Words Completed", str(s['words_completed']), TEXT_WHITE),
            ("Time Played", f"{s['time_played']:.1f}s", TEXT_DIM),
            ("Mode", mode, NEON_PURPLE),
        ]

        line_y = panel_y + 20
        for label, value, color in stats_lines:
            label_surf = small.render(label, True, TEXT_DIM)
            value_surf = font.render(value, True, color)
            surface.blit(label_surf, (panel_x + 30, line_y + 4))
            surface.blit(value_surf, (panel_x + panel_w - 30 - value_surf.get_width(), line_y))
            line_y += 36

        # Options
        options = ["Retry", "Main Menu", "Exit"]
        opt_y = panel_y + panel_h + 30
        for i, opt in enumerate(options):
            is_sel = (i == selected_index)
            color = NEON_CYAN if is_sel else TEXT_DIM
            prefix = "> " if is_sel else "  "
            surf = self.fonts["menu"].render(prefix + opt, True, color)
            rect = surf.get_rect(centerx=SCREEN_WIDTH // 2, top=opt_y + i * 45)
            surface.blit(surf, rect)

    # ── High Scores Screen ────────────────────────────────────────────────

    def draw_high_scores(self, surface, all_scores, selected_mode_index):
        """Draw the high scores screen."""
        header = self.fonts["result_title"]
        h_surf = header.render("HIGH SCORES", True, NEON_YELLOW)
        surface.blit(h_surf, h_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=40))

        # Mode tabs
        tab_y = 95
        tab_x_start = 60
        mode_names = list(ALL_MODES)
        for i, mode in enumerate(mode_names):
            is_sel = (i == selected_mode_index)
            short = mode.split()[0]  # First word
            color = NEON_CYAN if is_sel else TEXT_DIM
            surf = self.fonts["small"].render(short, True, color)
            x = tab_x_start + i * 200
            surface.blit(surf, (x, tab_y))
            if is_sel:
                pygame.draw.line(surface, NEON_CYAN, (x, tab_y + 18), (x + surf.get_width(), tab_y + 18), 2)

        # Scores list
        current_mode = mode_names[selected_mode_index]
        scores = all_scores.get(current_mode, [])

        list_y = 135
        font = self.fonts["result_small"]
        small = self.fonts["small"]

        # Header row
        headers = ["#", "Score", "WPM", "Accuracy", "Combo", "Date"]
        hx = [80, 150, 320, 450, 600, 750]
        for h, x in zip(headers, hx):
            surf = small.render(h, True, TEXT_DIM)
            surface.blit(surf, (x, list_y))
        list_y += 30

        if not scores:
            no_surf = font.render("No scores yet — go play!", True, TEXT_DIM)
            surface.blit(no_surf, no_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=list_y + 40))
        else:
            for i, entry in enumerate(scores[:10]):
                color = NEON_GREEN if i == 0 else TEXT_WHITE if i < 3 else TEXT_DIM
                vals = [
                    str(i + 1),
                    f"{entry.get('score', 0):,}",
                    f"{entry.get('wpm', 0):.1f}",
                    f"{entry.get('accuracy', 0):.1f}%",
                    f"x{entry.get('max_combo', 0)}",
                    entry.get("date", "—"),
                ]
                for v, x in zip(vals, hx):
                    surf = font.render(v, True, color)
                    surface.blit(surf, (x, list_y + i * 35))

        # Footer
        footer = self.fonts["small"]
        ft = footer.render("←/→ Switch Mode   ESC Back", True, TEXT_DIM)
        surface.blit(ft, ft.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 30))
