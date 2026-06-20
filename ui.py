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
    STATE_ACHIEVEMENTS, STATE_TUTORIAL,
    ALL_MODES, MODE_DESCRIPTIONS, ALL_DIFFICULTIES,
    FONT_MONO, FONT_MONO_FALLBACK, FONT_SANS, FONT_SANS_FALLBACK,
    ACHIEVEMENT_TOAST_DURATION, ACHIEVEMENT_TOAST_SLIDE_SPEED,
    POWERUP_CONFIG,
    WAVE_ANNOUNCEMENT_DURATION,
)


class UI:
    """Handles all game UI rendering."""

    def __init__(self):
        self.fonts = {}
        self.scanline_surface = None
        self.title_timer = 0.0
        self.cursor_blink = 0.0

        # Achievement toast state
        self.toast_active = None       # current toast dict
        self.toast_timer = 0           # frames remaining
        self.toast_y = -60             # slide-in y position

        # Wave announcement
        self.wave_announce_timer = 0
        self.wave_announce_number = 0

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

    def draw_hud(self, surface, player, stats, mode, time_left=None, wave_number=0):
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

        # ── Bottom: Enemies defeated + Wave ──
        ed_text = f"Defeated: {stats.enemies_defeated}"
        if wave_number > 0:
            ed_text += f"  |  Wave: {wave_number}"
        ed_surf = small.render(ed_text, True, TEXT_DIM)
        surface.blit(ed_surf, (SCREEN_WIDTH - ed_surf.get_width() - 20, SCREEN_HEIGHT - 35))

        # ── Active power-ups ──
        active_pups = player.get_active_powerups()
        if active_pups:
            pup_y = 70
            for pname, frames in active_pups:
                if frames < 0:
                    timer_str = f"{pname} [active]"
                else:
                    secs = frames // 60
                    timer_str = f"{pname} [{secs}s]"
                pup_color = NEON_CYAN
                if "SCORE" in pname:
                    pup_color = NEON_YELLOW
                elif "FREEZE" in pname:
                    pup_color = (150, 200, 255)
                pup_surf = small.render(timer_str, True, pup_color)
                surface.blit(pup_surf, (20, pup_y))
                pup_y += 18

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

    # ── Wave Announcement Banner ───────────────────────────────────────────

    def trigger_wave_announce(self, wave_number):
        """Start a wave announcement banner."""
        self.wave_announce_number = wave_number
        self.wave_announce_timer = WAVE_ANNOUNCEMENT_DURATION

    def draw_wave_announcement(self, surface):
        """Draw the wave announcement banner if active."""
        if self.wave_announce_timer <= 0:
            return
        self.wave_announce_timer -= 1

        progress = self.wave_announce_timer / WAVE_ANNOUNCEMENT_DURATION
        alpha = int(255 * min(1.0, progress * 3) * min(1.0, (1.0 - progress) * 3 + 0.3))

        font = self.fonts["result_title"]
        wave_text = f"WAVE {self.wave_announce_number}"

        r, g, b = NEON_CYAN
        faded = (max(0, min(255, int(r * alpha / 255))),
                 max(0, min(255, int(g * alpha / 255))),
                 max(0, min(255, int(b * alpha / 255))))

        # Glitch offset
        offset_x = int(math.sin(self.wave_announce_timer * 0.3) * 3)
        text_surf = font.render(wave_text, True, faded)
        text_rect = text_surf.get_rect(centerx=SCREEN_WIDTH // 2 + offset_x, centery=SCREEN_HEIGHT // 2 - 40)
        surface.blit(text_surf, text_rect)

        # Sub text
        sub = self.fonts["subtitle"]
        sub_faded = (max(0, min(255, int(TEXT_DIM[0] * alpha / 255))),
                     max(0, min(255, int(TEXT_DIM[1] * alpha / 255))),
                     max(0, min(255, int(TEXT_DIM[2] * alpha / 255))))
        sub_text = "Get ready..."
        sub_surf = sub.render(sub_text, True, sub_faded)
        sub_rect = sub_surf.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2)
        surface.blit(sub_surf, sub_rect)

    # ── Achievement Toast ─────────────────────────────────────────────

    def show_achievement_toast(self, achievement_def):
        """Trigger an achievement toast notification."""
        self.toast_active = achievement_def
        self.toast_timer = ACHIEVEMENT_TOAST_DURATION
        self.toast_y = -60

    def draw_achievement_toast(self, surface):
        """Draw the achievement toast sliding in from top."""
        if self.toast_active is None or self.toast_timer <= 0:
            self.toast_active = None
            return

        self.toast_timer -= 1

        # Slide in/out
        target_y = 10
        if self.toast_timer > ACHIEVEMENT_TOAST_DURATION - 20:
            # Sliding in
            self.toast_y += ACHIEVEMENT_TOAST_SLIDE_SPEED
            self.toast_y = min(self.toast_y, target_y)
        elif self.toast_timer < 20:
            # Sliding out
            self.toast_y -= ACHIEVEMENT_TOAST_SLIDE_SPEED
        else:
            self.toast_y = target_y

        if self.toast_y < -60:
            self.toast_active = None
            return

        # Toast panel
        toast_w = 360
        toast_h = 50
        toast_x = SCREEN_WIDTH // 2 - toast_w // 2

        pygame.draw.rect(surface, BG_PANEL, (toast_x, self.toast_y, toast_w, toast_h), border_radius=8)
        pygame.draw.rect(surface, NEON_YELLOW, (toast_x, self.toast_y, toast_w, toast_h), 2, border_radius=8)

        # Icon and text
        font = self.fonts["hud"]
        small = self.fonts["small"]

        icon_text = self.toast_active.get("icon", "[*]")
        icon_surf = font.render(icon_text, True, NEON_YELLOW)
        surface.blit(icon_surf, (toast_x + 15, self.toast_y + 8))

        title_surf = font.render("ACHIEVEMENT UNLOCKED", True, NEON_YELLOW)
        surface.blit(title_surf, (toast_x + 50, self.toast_y + 5))

        name_surf = small.render(self.toast_active.get("name", ""), True, TEXT_WHITE)
        surface.blit(name_surf, (toast_x + 50, self.toast_y + 28))

    # ── Achievements Screen ───────────────────────────────────────────

    def draw_achievements(self, surface, achievements_list, progress):
        """Draw the achievements screen."""
        header = self.fonts["result_title"]
        h_surf = header.render("ACHIEVEMENTS", True, NEON_YELLOW)
        surface.blit(h_surf, h_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=40))

        # Progress
        unlocked, total = progress
        prog_text = f"{unlocked}/{total} Unlocked"
        prog_surf = self.fonts["subtitle"].render(prog_text, True, TEXT_DIM)
        surface.blit(prog_surf, prog_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=85))

        # Achievement grid (2 columns)
        col_w = 550
        start_x = SCREEN_WIDTH // 2 - col_w
        start_y = 125
        font = self.fonts["hud"]
        small = self.fonts["small"]

        for i, (aid, defn, is_unlocked, date) in enumerate(achievements_list):
            col = i % 2
            row = i // 2
            x = start_x + col * col_w + 20
            y = start_y + row * 55

            # Panel
            panel_w = col_w - 40
            panel_h = 45
            bg = BG_PANEL_HOVER if is_unlocked else BG_PANEL
            border = NEON_YELLOW if is_unlocked else UI_BORDER
            pygame.draw.rect(surface, bg, (x, y, panel_w, panel_h), border_radius=5)
            pygame.draw.rect(surface, border, (x, y, panel_w, panel_h), 1, border_radius=5)

            # Icon
            icon_color = NEON_YELLOW if is_unlocked else TEXT_DIM
            icon_surf = font.render(defn.get("icon", "[?]"), True, icon_color)
            surface.blit(icon_surf, (x + 10, y + 6))

            # Name and description
            name_color = TEXT_WHITE if is_unlocked else TEXT_DIM
            name_surf = font.render(defn["name"], True, name_color)
            surface.blit(name_surf, (x + 50, y + 4))

            desc_color = TEXT_DIM
            desc_surf = small.render(defn["description"], True, desc_color)
            surface.blit(desc_surf, (x + 50, y + 26))

            # Date if unlocked
            if is_unlocked and date:
                date_surf = small.render(date, True, (80, 80, 100))
                surface.blit(date_surf, (x + panel_w - date_surf.get_width() - 10, y + 26))

        # Footer
        footer = self.fonts["small"]
        ft = footer.render("ESC Back", True, TEXT_DIM)
        surface.blit(ft, ft.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 30))

    # ── Tutorial / How To Play ─────────────────────────────────────────

    def draw_tutorial(self, surface, page_index):
        """Draw the tutorial/how-to-play screen."""
        pages = self._get_tutorial_pages()
        total_pages = len(pages)
        page = pages[page_index % total_pages]

        # Header
        header = self.fonts["result_title"]
        h_surf = header.render("HOW TO PLAY", True, NEON_CYAN)
        surface.blit(h_surf, h_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=40))

        # Page indicator
        page_text = f"Page {page_index + 1}/{total_pages}"
        page_surf = self.fonts["small"].render(page_text, True, TEXT_DIM)
        surface.blit(page_surf, page_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=82))

        # Page title
        title_surf = self.fonts["hud_large"].render(page["title"], True, page["color"])
        surface.blit(title_surf, title_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=115))

        # Content lines
        font = self.fonts["hud"]
        small = self.fonts["menu_small"]
        y = 165
        for line in page["lines"]:
            if line.startswith("!"):  # highlight line
                surf = font.render(line[1:], True, page["color"])
            elif line.startswith("#"):  # sub-header
                surf = font.render(line[1:], True, TEXT_WHITE)
            elif line == "":
                y += 10
                continue
            else:
                surf = small.render(line, True, TEXT_DIM)
            surface.blit(surf, surf.get_rect(centerx=SCREEN_WIDTH // 2, top=y))
            y += 28

        # Footer
        footer = self.fonts["small"]
        ft = footer.render("←/→ Switch Page   ESC Back", True, TEXT_DIM)
        surface.blit(ft, ft.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 30))

    def _get_tutorial_pages(self):
        """Return tutorial page content."""
        return [
            {
                "title": "CONTROLS",
                "color": NEON_CYAN,
                "lines": [
                    "#Keyboard Controls",
                    "",
                    "!Type characters to attack enemies",
                    "Each enemy has a word or code snippet above it",
                    "Type the text correctly to destroy the enemy",
                    "",
                    "!UP/DOWN arrows to navigate menus",
                    "!ENTER to select, ESC to pause or go back",
                    "",
                    "Typing auto-targets the first matching enemy",
                    "Complete the full word to fire a projectile",
                    "If an enemy reaches you, you lose HP!",
                ],
            },
            {
                "title": "SCORING & COMBOS",
                "color": NEON_YELLOW,
                "lines": [
                    "#Points System",
                    "",
                    "!10 points per correct character",
                    "!50 bonus per word completed",
                    "!200 bonus per boss defeated",
                    "",
                    "#Combo Multipliers",
                    "",
                    "!x2 at 2 streak  |  x3 at 5 streak",
                    "!x5 at 10 streak  |  x10 at 20 streak",
                    "",
                    "Wrong characters break your combo!",
                ],
            },
            {
                "title": "POWER-UPS",
                "color": NEON_GREEN,
                "lines": [
                    "#Defeated enemies may drop power-ups",
                    "",
                    "!SHIELD — Blocks the next damage hit",
                    "!+HP — Restores 1 health point",
                    "!FREEZE — Slows all enemies for 5 seconds",
                    "!2x SCORE — Double points for 10 seconds",
                    "!NUKE — Destroys all enemies on screen",
                    "",
                    "Power-ups auto-collect when near the player",
                ],
            },
            {
                "title": "ENEMY TYPES",
                "color": NEON_ORANGE,
                "lines": [
                    "#Watch out for special enemy variants!",
                    "",
                    "!FAST (orange) — Moves 1.5x faster",
                    "!ARMORED (grey) — Takes 2 hits to destroy",
                    "!SPLITTER (green) — Splits into 2 on defeat",
                    "!BOSS (purple) — Long text, 3 HP",
                    "",
                    "Enemies get faster and harder each wave",
                    "Every 3rd wave features a boss enemy",
                ],
            },
            {
                "title": "GAME MODES",
                "color": NEON_PURPLE,
                "lines": [
                    "!Classic Survival — Endless waves until HP = 0",
                    "!Time Attack — Maximize score in 120 seconds",
                    "!Boss Rush — Long Python snippets, tough bosses",
                    "!Debug Mode — Fix broken Python code",
                    "!Command Line — Terminal commands only",
                    "!Interview Mode — DSA terms and concepts",
                    "",
                    "Select mode from the main menu",
                    "Unlock achievements by playing different modes!",
                ],
            },
        ]
