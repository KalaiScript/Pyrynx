"""
Typing Takedown — Stats Tracker
Real-time WPM, accuracy, combo, and streak tracking.
"""

import time
from settings import COMBO_THRESHOLDS


class Stats:
    """Tracks all gameplay statistics in real-time."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all stats for a new game."""
        self.start_time = None
        self.total_chars_typed = 0
        self.correct_chars = 0
        self.wrong_chars = 0
        self.words_completed = 0
        self.enemies_defeated = 0
        self.combo = 0             # current combo streak
        self.max_combo = 0         # best combo this game
        self.multiplier = 1        # current score multiplier
        self.score = 0
        self.boss_kills = 0
        self.waves_survived = 0    # waves completed
        self.powerups_collected = 0

    def start(self):
        """Mark the start of gameplay for WPM calculation."""
        self.start_time = time.time()

    def get_elapsed_seconds(self) -> float:
        """Get seconds since game started."""
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time

    def get_elapsed_minutes(self) -> float:
        """Get minutes since game started (minimum 1/60 to avoid division by zero)."""
        return max(self.get_elapsed_seconds() / 60.0, 1.0 / 60.0)

    def get_wpm(self) -> float:
        """
        Calculate Words Per Minute.
        Standard: 1 word = 5 characters.
        """
        if self.correct_chars == 0:
            return 0.0
        words = self.correct_chars / 5.0
        return round(words / self.get_elapsed_minutes(), 1)

    def get_accuracy(self) -> float:
        """Get accuracy percentage."""
        total = self.total_chars_typed
        if total == 0:
            return 100.0
        return round((self.correct_chars / total) * 100.0, 1)

    def record_correct_char(self):
        """Record a correctly typed character."""
        self.total_chars_typed += 1
        self.correct_chars += 1

    def record_wrong_char(self):
        """Record an incorrectly typed character."""
        self.total_chars_typed += 1
        self.wrong_chars += 1

    def record_word_complete(self, score_earned: int):
        """Record a completed word and update combo."""
        self.words_completed += 1
        self.combo += 1
        self.max_combo = max(self.max_combo, self.combo)
        self._update_multiplier()
        actual_score = int(score_earned * self.multiplier)
        self.score += actual_score
        return actual_score

    def record_enemy_defeated(self, is_boss: bool = False):
        """Record an enemy kill."""
        self.enemies_defeated += 1
        if is_boss:
            self.boss_kills += 1

    def break_combo(self):
        """Reset combo on a miss (wrong character)."""
        self.combo = 0
        self.multiplier = 1

    def _update_multiplier(self):
        """Update score multiplier based on combo thresholds."""
        self.multiplier = 1
        for threshold, mult in sorted(COMBO_THRESHOLDS.items()):
            if self.combo >= threshold:
                self.multiplier = mult
            else:
                break

    def add_raw_score(self, points: int):
        """Add score without multiplier (e.g., time bonuses)."""
        self.score += points

    def record_wave_complete(self):
        """Record a wave completion."""
        self.waves_survived += 1

    def record_powerup(self):
        """Record a power-up collection."""
        self.powerups_collected += 1

    def get_summary(self) -> dict:
        """Get a summary dict of all stats for game-over display."""
        return {
            "score": self.score,
            "wpm": self.get_wpm(),
            "accuracy": self.get_accuracy(),
            "max_combo": self.max_combo,
            "enemies_defeated": self.enemies_defeated,
            "boss_kills": self.boss_kills,
            "words_completed": self.words_completed,
            "correct_chars": self.correct_chars,
            "wrong_chars": self.wrong_chars,
            "time_played": round(self.get_elapsed_seconds(), 1),
            "waves_survived": self.waves_survived,
            "powerups_collected": self.powerups_collected,
        }
