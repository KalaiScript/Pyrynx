"""
Typing Takedown — Achievements System
Unlockable achievements with persistent tracking.
"""

import json
import os
from datetime import datetime

ACHIEVEMENTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "achievements.json")

# Achievement definitions: id -> {name, description, icon, condition_desc}
ACHIEVEMENT_DEFS = {
    "first_blood": {
        "name": "First Blood",
        "description": "Defeat your first enemy",
        "icon": "[*]",
    },
    "speed_demon": {
        "name": "Speed Demon",
        "description": "Reach 80+ WPM in a game",
        "icon": "[!]",
    },
    "perfectionist": {
        "name": "Perfectionist",
        "description": "100% accuracy with 10+ words",
        "icon": "[o]",
    },
    "combo_master": {
        "name": "Combo Master",
        "description": "Achieve x10 combo multiplier",
        "icon": "[#]",
    },
    "boss_slayer": {
        "name": "Boss Slayer",
        "description": "Defeat 5 bosses total",
        "icon": "[^]",
    },
    "centurion": {
        "name": "Centurion",
        "description": "Score 10,000+ in one game",
        "icon": "[%]",
    },
    "survivor": {
        "name": "Survivor",
        "description": "Survive 10 waves",
        "icon": "[=]",
    },
    "debugger": {
        "name": "Debugger",
        "description": "Complete a Debug Mode game",
        "icon": "[~]",
    },
    "terminal_hacker": {
        "name": "Terminal Hacker",
        "description": "Complete a Command Line game",
        "icon": "[$]",
    },
    "polyglot": {
        "name": "Polyglot",
        "description": "Play all 6 game modes",
        "icon": "[@]",
    },
    "unstoppable": {
        "name": "Unstoppable",
        "description": "Defeat 50 enemies in one game",
        "icon": "[&]",
    },
    "marathon": {
        "name": "Marathon",
        "description": "Play for 5+ minutes in one game",
        "icon": "[+]",
    },
}

ALL_ACHIEVEMENT_IDS = list(ACHIEVEMENT_DEFS.keys())


class AchievementManager:
    """Manages achievement state, unlocking, and persistence."""

    def __init__(self):
        self.unlocked = {}       # id -> {"date": ...}
        self.modes_played = set()
        self.total_boss_kills = 0
        self.pending_toasts = []  # achievements to show as toasts
        self._load()

    def _load(self):
        """Load achievement state from disk."""
        if not os.path.exists(ACHIEVEMENTS_FILE):
            return
        try:
            with open(ACHIEVEMENTS_FILE, "r") as f:
                data = json.load(f)
            self.unlocked = data.get("unlocked", {})
            self.modes_played = set(data.get("modes_played", []))
            self.total_boss_kills = data.get("total_boss_kills", 0)
        except (json.JSONDecodeError, IOError):
            pass

    def _save(self):
        """Save achievement state to disk."""
        data = {
            "unlocked": self.unlocked,
            "modes_played": list(self.modes_played),
            "total_boss_kills": self.total_boss_kills,
        }
        try:
            with open(ACHIEVEMENTS_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except IOError:
            pass

    def _unlock(self, achievement_id):
        """Unlock an achievement if not already unlocked."""
        if achievement_id in self.unlocked:
            return False
        if achievement_id not in ACHIEVEMENT_DEFS:
            return False
        self.unlocked[achievement_id] = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self.pending_toasts.append(achievement_id)
        self._save()
        return True

    def pop_toast(self):
        """Pop the next achievement toast to display, or None."""
        if self.pending_toasts:
            aid = self.pending_toasts.pop(0)
            return ACHIEVEMENT_DEFS.get(aid)
        return None

    def is_unlocked(self, achievement_id):
        return achievement_id in self.unlocked

    def get_progress(self):
        """Get (unlocked_count, total_count)."""
        return len(self.unlocked), len(ACHIEVEMENT_DEFS)

    def get_all_with_status(self):
        """Get list of (id, definition, is_unlocked, date) for display."""
        result = []
        for aid, defn in ACHIEVEMENT_DEFS.items():
            is_u = aid in self.unlocked
            date = self.unlocked.get(aid, {}).get("date", "")
            result.append((aid, defn, is_u, date))
        return result

    # ── Check functions (called from game.py) ─────────────────────────────

    def check_enemy_defeated(self, stats, is_boss=False):
        """Check achievements related to defeating enemies."""
        if stats.enemies_defeated >= 1:
            self._unlock("first_blood")
        if stats.enemies_defeated >= 50:
            self._unlock("unstoppable")
        if is_boss:
            self.total_boss_kills += 1
            if self.total_boss_kills >= 5:
                self._unlock("boss_slayer")
            self._save()

    def check_combo(self, combo, multiplier):
        """Check combo-related achievements."""
        if multiplier >= 10:
            self._unlock("combo_master")

    def check_game_over(self, stats, mode, wave_number=0):
        """Check achievements at end of game."""
        from settings import MODE_DEBUG, MODE_COMMAND_LINE

        if stats.get_wpm() >= 80:
            self._unlock("speed_demon")
        if stats.get_accuracy() >= 100.0 and stats.words_completed >= 10:
            self._unlock("perfectionist")
        if stats.score >= 10000:
            self._unlock("centurion")
        if stats.get_elapsed_seconds() >= 300:
            self._unlock("marathon")
        if wave_number >= 10:
            self._unlock("survivor")

        # Mode-specific
        if mode == MODE_DEBUG and stats.enemies_defeated > 0:
            self._unlock("debugger")
        if mode == MODE_COMMAND_LINE and stats.enemies_defeated > 0:
            self._unlock("terminal_hacker")

        # Track modes played
        self.modes_played.add(mode)
        if len(self.modes_played) >= 6:
            self._unlock("polyglot")
        self._save()
