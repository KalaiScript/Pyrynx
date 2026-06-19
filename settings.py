"""
Typing Takedown — Settings & Constants
Game configuration, color palette, difficulty presets, and state definitions.
"""

import pygame

# ─── Display ──────────────────────────────────────────────────────────────────
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Typing Takedown"

# ─── Game States ──────────────────────────────────────────────────────────────
STATE_MENU = "menu"
STATE_MODE_SELECT = "mode_select"
STATE_DIFFICULTY_SELECT = "difficulty_select"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
STATE_HIGH_SCORES = "high_scores"

# ─── Game Modes ───────────────────────────────────────────────────────────────
MODE_CLASSIC = "Classic Survival"
MODE_TIME_ATTACK = "Time Attack"
MODE_BOSS_RUSH = "Boss Rush"
MODE_DEBUG = "Debug Mode"
MODE_COMMAND_LINE = "Command Line"
MODE_INTERVIEW = "Interview Mode"

ALL_MODES = [
    MODE_CLASSIC,
    MODE_TIME_ATTACK,
    MODE_BOSS_RUSH,
    MODE_DEBUG,
    MODE_COMMAND_LINE,
    MODE_INTERVIEW,
]

MODE_DESCRIPTIONS = {
    MODE_CLASSIC: "Survive endless waves of Python enemies",
    MODE_TIME_ATTACK: "Maximize your score in 120 seconds",
    MODE_BOSS_RUSH: "Face long, brutal code snippets",
    MODE_DEBUG: "Fix broken Python code to survive",
    MODE_COMMAND_LINE: "Terminal commands only — hack your way out",
    MODE_INTERVIEW: "DSA terms and Python concepts",
}

# ─── Cyberpunk Color Palette ──────────────────────────────────────────────────
# Backgrounds
BG_DARK = (10, 10, 15)
BG_PANEL = (18, 18, 28)
BG_PANEL_HOVER = (28, 28, 42)
BG_ENEMY = (15, 20, 30)
BG_ENEMY_TARGETED = (20, 30, 50)

# Neon accents
NEON_GREEN = (0, 255, 136)
NEON_CYAN = (0, 229, 255)
NEON_MAGENTA = (255, 0, 102)
NEON_YELLOW = (255, 230, 0)
NEON_PURPLE = (170, 0, 255)
NEON_ORANGE = (255, 140, 0)

# Text colors
TEXT_WHITE = (230, 230, 240)
TEXT_DIM = (120, 120, 140)
TEXT_CORRECT = NEON_GREEN
TEXT_WRONG = NEON_MAGENTA
TEXT_PENDING = (80, 80, 100)
TEXT_CURSOR = NEON_CYAN

# UI
UI_HEALTH_FULL = NEON_GREEN
UI_HEALTH_MID = NEON_YELLOW
UI_HEALTH_LOW = NEON_MAGENTA
UI_COMBO = NEON_CYAN
UI_SCORE = NEON_GREEN
UI_BORDER = (40, 40, 60)
UI_BORDER_GLOW = NEON_CYAN

# Particle colors
PARTICLE_DESTROY = [NEON_GREEN, NEON_CYAN, (100, 255, 200)]
PARTICLE_DAMAGE = [NEON_MAGENTA, (255, 80, 80), NEON_ORANGE]
PARTICLE_COMBO = [NEON_YELLOW, NEON_ORANGE, (255, 255, 150)]
PARTICLE_MATRIX = [(0, 180, 80), (0, 220, 100), (0, 140, 60)]

# ─── Difficulty Presets ───────────────────────────────────────────────────────
DIFFICULTY_EASY = "Easy"
DIFFICULTY_MEDIUM = "Medium"
DIFFICULTY_HARD = "Hard"

ALL_DIFFICULTIES = [DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_HARD]

DIFFICULTY_CONFIG = {
    DIFFICULTY_EASY: {
        "spawn_rate_ms": 3500,         # ms between enemy spawns
        "spawn_rate_min_ms": 1800,     # minimum spawn rate (after scaling)
        "enemy_speed": 0.4,            # pixels per frame
        "enemy_speed_max": 1.0,        # max speed after scaling
        "word_complexity": "easy",     # text_bank difficulty tier
        "max_enemies": 5,              # max simultaneous enemies
        "player_health": 7,
        "boss_interval": 15,           # enemies between bosses
        "speed_scale_rate": 0.002,     # speed increase per second
        "spawn_scale_rate": 2,         # ms decrease in spawn rate per second
        "time_attack_seconds": 120,
    },
    DIFFICULTY_MEDIUM: {
        "spawn_rate_ms": 2800,
        "spawn_rate_min_ms": 1200,
        "enemy_speed": 0.55,
        "enemy_speed_max": 1.4,
        "word_complexity": "medium",
        "max_enemies": 7,
        "player_health": 5,
        "boss_interval": 12,
        "speed_scale_rate": 0.003,
        "spawn_scale_rate": 3,
        "time_attack_seconds": 120,
    },
    DIFFICULTY_HARD: {
        "spawn_rate_ms": 2000,
        "spawn_rate_min_ms": 800,
        "enemy_speed": 0.7,
        "enemy_speed_max": 1.8,
        "word_complexity": "hard",
        "max_enemies": 10,
        "player_health": 3,
        "boss_interval": 8,
        "speed_scale_rate": 0.005,
        "spawn_scale_rate": 5,
        "time_attack_seconds": 90,
    },
}

# ─── Scoring ──────────────────────────────────────────────────────────────────
SCORE_PER_CHAR = 10
SCORE_WORD_BONUS = 50
SCORE_BOSS_BONUS = 200

COMBO_THRESHOLDS = {
    2: 2,    # 2 words in a row = x2
    5: 3,    # 5 words in a row = x3
    10: 5,   # 10 words in a row = x5
    20: 10,  # 20 words in a row = x10
}

# ─── Player ───────────────────────────────────────────────────────────────────
PLAYER_Y = SCREEN_HEIGHT - 80
PLAYER_X = SCREEN_WIDTH // 2
PLAYER_WIDTH = 120
PLAYER_HEIGHT = 50

# ─── Enemy ────────────────────────────────────────────────────────────────────
ENEMY_WIDTH_MIN = 120
ENEMY_HEIGHT = 40
ENEMY_PADDING = 12
ENEMY_SPAWN_Y = -60
ENEMY_KILL_Y = SCREEN_HEIGHT - 120  # y-position where enemy damages player
ENEMY_BOSS_HP = 3

# ─── Projectile ──────────────────────────────────────────────────────────────
PROJECTILE_SPEED = 12
PROJECTILE_LENGTH = 20
PROJECTILE_WIDTH = 3

# ─── Screen Shake ─────────────────────────────────────────────────────────────
SHAKE_INTENSITY = 8
SHAKE_DURATION_MS = 300

# ─── Fonts (system monospace) ─────────────────────────────────────────────────
FONT_MONO = "consolas"
FONT_MONO_FALLBACK = "couriernew"
FONT_SANS = "segoeui"
FONT_SANS_FALLBACK = "dejavusans"

# ─── Scanline overlay ────────────────────────────────────────────────────────
SCANLINE_ALPHA = 15
SCANLINE_GAP = 3
