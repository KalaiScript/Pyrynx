"""
Typing Takedown — Core Game Loop
State machine, enemy spawning, input routing, and the main update/render cycle.
"""

import pygame
import random
import time
import math

from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, BG_DARK,
    STATE_MENU, STATE_MODE_SELECT, STATE_DIFFICULTY_SELECT,
    STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER, STATE_HIGH_SCORES,
    MODE_CLASSIC, MODE_TIME_ATTACK, MODE_BOSS_RUSH,
    MODE_DEBUG, MODE_COMMAND_LINE, MODE_INTERVIEW,
    ALL_MODES, ALL_DIFFICULTIES,
    DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_HARD,
    DIFFICULTY_CONFIG,
    SCORE_PER_CHAR, SCORE_WORD_BONUS, SCORE_BOSS_BONUS,
    NEON_GREEN, NEON_CYAN, NEON_MAGENTA, NEON_YELLOW, NEON_PURPLE,
    PLAYER_X, PLAYER_Y,
    SHAKE_INTENSITY, SHAKE_DURATION_MS,
    ENEMY_KILL_Y,
)
from player import Player
from enemy import Enemy
from projectile import Projectile
from particle import ParticleSystem
from text_bank import get_word_for_mode, get_boss_word
from stats import Stats
from scores import save_score, get_top_score, is_new_high_score, get_all_high_scores
from sound_manager import SoundManager
from ui import UI


class Game:
    """Main game class — manages states, objects, and the game loop."""

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        # State
        self.state = STATE_MENU
        self.mode = MODE_CLASSIC
        self.difficulty = DIFFICULTY_MEDIUM

        # Menu navigation
        self.menu_items = ["Play", "Mode", "Difficulty", "High Scores", "Exit"]
        self.menu_index = 0
        self.mode_index = 0
        self.diff_index = 1  # Default Medium
        self.pause_index = 0
        self.gameover_index = 0
        self.highscore_mode_index = 0

        # Systems
        self.ui = UI()
        self.ui.init()
        self.sound = SoundManager()
        self.sound.init()
        self.particles = ParticleSystem()
        self.particles.init_fonts(
            self.ui.get_font("small"),
            self.ui.get_font("float"),
        )

        # Game objects
        self.player = Player()
        self.enemies = []
        self.projectiles = []
        self.stats = Stats()

        # Input state
        self.current_input = ""
        self.targeted_enemy = None

        # Spawning
        self.spawn_timer = 0
        self.enemies_spawned = 0
        self.difficulty_config = {}

        # Screen shake
        self.shake_offset = (0, 0)
        self.shake_timer = 0
        self.shake_start = 0

        # Time Attack
        self.time_left = 0

        # Game over
        self.final_stats = {}
        self.new_high = False

    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS)
            self._handle_events()
            self._update(dt)
            self._render()
        pygame.quit()

    # ── Event Handling ────────────────────────────────────────────────────

    def _handle_events(self):
        """Process all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                if self.state == STATE_MENU:
                    self._handle_menu_input(event)
                elif self.state == STATE_MODE_SELECT:
                    self._handle_mode_select_input(event)
                elif self.state == STATE_DIFFICULTY_SELECT:
                    self._handle_difficulty_select_input(event)
                elif self.state == STATE_PLAYING:
                    self._handle_gameplay_input(event)
                elif self.state == STATE_PAUSED:
                    self._handle_pause_input(event)
                elif self.state == STATE_GAME_OVER:
                    self._handle_gameover_input(event)
                elif self.state == STATE_HIGH_SCORES:
                    self._handle_highscores_input(event)

    def _handle_menu_input(self, event):
        if event.key == pygame.K_UP:
            self.menu_index = (self.menu_index - 1) % len(self.menu_items)
            self.sound.play("navigate")
        elif event.key == pygame.K_DOWN:
            self.menu_index = (self.menu_index + 1) % len(self.menu_items)
            self.sound.play("navigate")
        elif event.key == pygame.K_RETURN:
            self.sound.play("select")
            item = self.menu_items[self.menu_index]
            if item == "Play":
                self._start_game()
            elif item == "Mode":
                self.state = STATE_MODE_SELECT
                self.mode_index = ALL_MODES.index(self.mode) if self.mode in ALL_MODES else 0
            elif item == "Difficulty":
                self.state = STATE_DIFFICULTY_SELECT
                self.diff_index = ALL_DIFFICULTIES.index(self.difficulty) if self.difficulty in ALL_DIFFICULTIES else 1
            elif item == "High Scores":
                self.state = STATE_HIGH_SCORES
                self.highscore_mode_index = 0
            elif item == "Exit":
                self.running = False
        elif event.key == pygame.K_ESCAPE:
            self.running = False

    def _handle_mode_select_input(self, event):
        if event.key == pygame.K_UP:
            self.mode_index = (self.mode_index - 1) % len(ALL_MODES)
            self.sound.play("navigate")
        elif event.key == pygame.K_DOWN:
            self.mode_index = (self.mode_index + 1) % len(ALL_MODES)
            self.sound.play("navigate")
        elif event.key == pygame.K_RETURN:
            self.mode = ALL_MODES[self.mode_index]
            self.sound.play("select")
            self.state = STATE_MENU
        elif event.key == pygame.K_ESCAPE:
            self.state = STATE_MENU

    def _handle_difficulty_select_input(self, event):
        if event.key == pygame.K_UP:
            self.diff_index = (self.diff_index - 1) % len(ALL_DIFFICULTIES)
            self.sound.play("navigate")
        elif event.key == pygame.K_DOWN:
            self.diff_index = (self.diff_index + 1) % len(ALL_DIFFICULTIES)
            self.sound.play("navigate")
        elif event.key == pygame.K_RETURN:
            self.difficulty = ALL_DIFFICULTIES[self.diff_index]
            self.sound.play("select")
            self.state = STATE_MENU
        elif event.key == pygame.K_ESCAPE:
            self.state = STATE_MENU

    def _handle_gameplay_input(self, event):
        if event.key == pygame.K_ESCAPE:
            self.state = STATE_PAUSED
            self.pause_index = 0
            return

        # Get the typed character
        char = event.unicode
        if not char or not char.isprintable():
            return

        self.sound.play("keypress")

        # If no targeted enemy, try to find one that starts with this char
        if self.targeted_enemy is None or not self.targeted_enemy.alive:
            self.targeted_enemy = None
            for enemy in self.enemies:
                if enemy.alive and enemy.matches_start(char):
                    self.targeted_enemy = enemy
                    enemy.targeted = True
                    break

        if self.targeted_enemy is None:
            # No matching enemy — record as wrong if there are enemies
            if self.enemies:
                self.stats.record_wrong_char()
                self.stats.break_combo()
                self.sound.play("wrong")
            return

        # Check input against targeted enemy
        correct = self.targeted_enemy.check_input(char)

        if correct:
            self.stats.record_correct_char()
            self.current_input += char
            self.sound.play("correct")

            # Sparkle at enemy position
            ex, ey = self.targeted_enemy.get_center()
            self.particles.spawn_correct_sparkle(ex, ey)

            # Check if word is complete
            if self.targeted_enemy.is_complete():
                self._on_enemy_defeated(self.targeted_enemy)
        else:
            self.stats.record_wrong_char()
            self.stats.break_combo()
            self.sound.play("wrong")

            # Wrong flash particles
            ex, ey = self.targeted_enemy.get_center()
            self.particles.spawn_wrong_flash(ex, ey)

    def _handle_pause_input(self, event):
        if event.key == pygame.K_ESCAPE:
            self.state = STATE_PLAYING
        elif event.key == pygame.K_UP:
            self.pause_index = (self.pause_index - 1) % 3
            self.sound.play("navigate")
        elif event.key == pygame.K_DOWN:
            self.pause_index = (self.pause_index + 1) % 3
            self.sound.play("navigate")
        elif event.key == pygame.K_RETURN:
            self.sound.play("select")
            if self.pause_index == 0:  # Resume
                self.state = STATE_PLAYING
            elif self.pause_index == 1:  # Restart
                self._start_game()
            elif self.pause_index == 2:  # Main Menu
                self.state = STATE_MENU

    def _handle_gameover_input(self, event):
        if event.key == pygame.K_UP:
            self.gameover_index = (self.gameover_index - 1) % 3
            self.sound.play("navigate")
        elif event.key == pygame.K_DOWN:
            self.gameover_index = (self.gameover_index + 1) % 3
            self.sound.play("navigate")
        elif event.key == pygame.K_RETURN:
            self.sound.play("select")
            if self.gameover_index == 0:  # Retry
                self._start_game()
            elif self.gameover_index == 1:  # Main Menu
                self.state = STATE_MENU
            elif self.gameover_index == 2:  # Exit
                self.running = False

    def _handle_highscores_input(self, event):
        if event.key == pygame.K_ESCAPE:
            self.state = STATE_MENU
        elif event.key == pygame.K_LEFT:
            self.highscore_mode_index = (self.highscore_mode_index - 1) % len(ALL_MODES)
            self.sound.play("navigate")
        elif event.key == pygame.K_RIGHT:
            self.highscore_mode_index = (self.highscore_mode_index + 1) % len(ALL_MODES)
            self.sound.play("navigate")

    # ── Game Start / End ──────────────────────────────────────────────────

    def _start_game(self):
        """Initialize a new game session."""
        self.difficulty_config = DIFFICULTY_CONFIG[self.difficulty].copy()
        self.player.reset(self.difficulty_config["player_health"])
        self.enemies.clear()
        self.projectiles.clear()
        self.particles.clear()
        self.stats.reset()
        self.stats.start()
        self.current_input = ""
        self.targeted_enemy = None
        self.spawn_timer = 0
        self.enemies_spawned = 0
        self.shake_timer = 0

        if self.mode == MODE_TIME_ATTACK:
            self.time_left = self.difficulty_config["time_attack_seconds"]
        else:
            self.time_left = 0

        self.state = STATE_PLAYING

    def _end_game(self):
        """End the current game and show results."""
        self.final_stats = self.stats.get_summary()
        self.new_high = is_new_high_score(self.mode, self.final_stats["score"])
        save_score(self.mode, self.final_stats)
        self.sound.play("gameover")
        self.gameover_index = 0
        self.state = STATE_GAME_OVER

    # ── Enemy Spawning ────────────────────────────────────────────────────

    def _spawn_enemy(self):
        """Spawn a new enemy based on mode and difficulty."""
        cfg = self.difficulty_config
        complexity = cfg["word_complexity"]

        # Check if this should be a boss
        is_boss = (
            self.enemies_spawned > 0
            and self.enemies_spawned % cfg["boss_interval"] == 0
            and self.mode != MODE_TIME_ATTACK
        )

        if self.mode == MODE_BOSS_RUSH:
            is_boss = True

        # Get word
        word_data = get_word_for_mode(self.mode, complexity, is_boss)

        if self.mode == MODE_DEBUG and isinstance(word_data, tuple):
            broken, correct = word_data
            enemy = Enemy(
                text=correct,
                speed=cfg["enemy_speed"],
                is_boss=False,
                debug_display=broken,
            )
        else:
            text = word_data if isinstance(word_data, str) else str(word_data)
            speed = cfg["enemy_speed"] * (0.6 if is_boss else 1.0)
            enemy = Enemy(text=text, speed=speed, is_boss=is_boss)

        # Avoid overlapping with existing enemies
        attempts = 0
        while attempts < 10:
            overlap = False
            for e in self.enemies:
                if (abs(enemy.x - e.x) < enemy.text_width + 20
                        and abs(enemy.y - e.y) < enemy.height + 20):
                    overlap = True
                    break
            if not overlap:
                break
            enemy.x = random.randint(40, max(41, SCREEN_WIDTH - enemy.text_width - 40))
            attempts += 1

        self.enemies.append(enemy)
        self.enemies_spawned += 1

        if is_boss:
            self.sound.play("boss")

    def _on_enemy_defeated(self, enemy):
        """Handle enemy destruction."""
        # Score
        char_score = len(enemy.text) * SCORE_PER_CHAR
        bonus = SCORE_BOSS_BONUS if enemy.is_boss else SCORE_WORD_BONUS
        total = char_score + bonus
        actual = self.stats.record_word_complete(total)
        self.stats.record_enemy_defeated(enemy.is_boss)

        # Fire projectile from player to enemy
        px, py = self.player.get_center()
        ex, ey = enemy.get_center()
        proj_color = NEON_PURPLE if enemy.is_boss else NEON_GREEN
        self.projectiles.append(Projectile(px, py, ex, ey, proj_color))

        # Particles
        self.particles.spawn_explosion(ex, ey)
        self.particles.add_floating_text(
            f"+{actual}", ex, ey - 20, NEON_GREEN,
        )

        # Combo milestone effects
        if self.stats.combo in [2, 5, 10, 20]:
            self.particles.spawn_combo_effect(ex, ey - 30)
            self.particles.add_floating_text(
                f"COMBO x{self.stats.multiplier}!", ex, ey - 50, NEON_YELLOW, 80,
            )
            self.sound.play("combo")
        else:
            self.sound.play("destroy")

        # Clear targeting
        enemy.alive = False
        enemy.targeted = False
        self.targeted_enemy = None
        self.current_input = ""

    # ── Update ────────────────────────────────────────────────────────────

    def _update(self, dt):
        """Update all game objects."""
        if self.state != STATE_PLAYING:
            # Still update particles for visual effects on menus
            self.particles.update()
            return

        # Difficulty scaling over time
        elapsed = self.stats.get_elapsed_seconds()
        cfg = self.difficulty_config
        cfg["enemy_speed"] = min(
            cfg["enemy_speed_max"],
            DIFFICULTY_CONFIG[self.difficulty]["enemy_speed"] + elapsed * cfg["speed_scale_rate"],
        )
        current_spawn = max(
            cfg["spawn_rate_min_ms"],
            DIFFICULTY_CONFIG[self.difficulty]["spawn_rate_ms"] - elapsed * cfg["spawn_scale_rate"],
        )

        # Time Attack countdown
        if self.mode == MODE_TIME_ATTACK:
            self.time_left -= dt / 1000.0
            if self.time_left <= 0:
                self.time_left = 0
                self._end_game()
                return

        # Spawn timer
        self.spawn_timer += dt
        if self.spawn_timer >= current_spawn and len(self.enemies) < cfg["max_enemies"]:
            self.spawn_timer = 0
            self._spawn_enemy()

        # Update player
        self.player.update()

        # Update enemies
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            enemy.update()

            # Check if enemy reached player
            if enemy.has_reached_player():
                damage_applied = self.player.take_damage()
                if damage_applied:
                    self.sound.play("damage")
                    self._trigger_shake()
                    self.particles.spawn_damage_effect(
                        self.player.x, self.player.y,
                    )
                    self.stats.break_combo()

                # If this was the targeted enemy, clear targeting
                if enemy == self.targeted_enemy:
                    self.targeted_enemy = None
                    self.current_input = ""

                enemy.alive = False

        # Remove dead enemies
        self.enemies = [e for e in self.enemies if e.alive]

        # Update projectiles
        for proj in self.projectiles:
            proj.update()
        self.projectiles = [p for p in self.projectiles if p.alive or p.trail]

        # Update particles
        self.particles.update()

        # Update screen shake
        if self.shake_timer > 0:
            elapsed_shake = pygame.time.get_ticks() - self.shake_start
            if elapsed_shake > SHAKE_DURATION_MS:
                self.shake_timer = 0
                self.shake_offset = (0, 0)
            else:
                intensity = SHAKE_INTENSITY * (1.0 - elapsed_shake / SHAKE_DURATION_MS)
                self.shake_offset = (
                    random.randint(-int(intensity), int(intensity)),
                    random.randint(-int(intensity), int(intensity)),
                )

        # Check game over
        if not self.player.alive:
            self._end_game()

    def _trigger_shake(self):
        """Start screen shake effect."""
        self.shake_timer = 1
        self.shake_start = pygame.time.get_ticks()

    # ── Render ────────────────────────────────────────────────────────────

    def _render(self):
        """Render the current frame."""
        # Create render surface (for shake offset)
        render_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        render_surface.fill(BG_DARK)

        # Matrix rain background (always)
        self.particles.draw_matrix_rain(render_surface)

        if self.state == STATE_MENU:
            self.ui.draw_menu(render_surface, self.menu_index, self.menu_items)

        elif self.state == STATE_MODE_SELECT:
            self.ui.draw_mode_select(render_surface, self.mode_index)

        elif self.state == STATE_DIFFICULTY_SELECT:
            self.ui.draw_difficulty_select(render_surface, self.diff_index)

        elif self.state == STATE_PLAYING:
            self._render_gameplay(render_surface)

        elif self.state == STATE_PAUSED:
            self._render_gameplay(render_surface)
            self.ui.draw_pause(render_surface, self.pause_index)

        elif self.state == STATE_GAME_OVER:
            self._render_gameplay(render_surface)
            self.ui.draw_game_over(
                render_surface, self.final_stats, self.mode,
                self.new_high, self.gameover_index,
            )

        elif self.state == STATE_HIGH_SCORES:
            all_scores = get_all_high_scores()
            self.ui.draw_high_scores(render_surface, all_scores, self.highscore_mode_index)

        # Scanline overlay
        self.ui.draw_scanlines(render_surface)

        # Apply shake offset and blit to screen
        self.screen.blit(render_surface, self.shake_offset)
        pygame.display.flip()

    def _render_gameplay(self, surface):
        """Render the gameplay elements."""
        font_code = self.ui.get_font("code")
        font_small = self.ui.get_font("small")

        # Draw enemies
        for enemy in self.enemies:
            if enemy.alive:
                enemy.draw(surface, font_code, font_small)

        # Draw projectiles
        for proj in self.projectiles:
            proj.draw(surface)

        # Draw particles
        self.particles.draw(surface)

        # Draw player
        self.player.draw(surface)

        # Draw input display
        self.ui.draw_input_display(surface, self.current_input, self.targeted_enemy)

        # Draw HUD
        time_left = self.time_left if self.mode == MODE_TIME_ATTACK else None
        self.ui.draw_hud(surface, self.player, self.stats, self.mode, time_left)
