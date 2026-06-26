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
        self.start_time = None          # set when gameplay begins via start()

        # Keystroke counters
        self.total_chars_typed = 0      # every keypress (correct + wrong)
        self.correct_chars = 0          # correctly typed characters only
        self.wrong_chars = 0            # incorrectly typed characters

        # Word / enemy tracking
        self.words_completed = 0        # words typed to completion
        self.enemies_defeated = 0       # total enemies destroyed
        self.boss_kills = 0             # boss-specific kill count

        # Combo & scoring
        self.combo = 0                  # current consecutive word streak
        self.max_combo = 0              # highest streak reached this game
        self.multiplier = 1             # current score multiplier (1×, 2×, 3×, 5×, 10×)
        self.score = 0                  # cumulative game score

        # Progress tracking
        self.waves_survived = 0         # number of waves fully cleared
        self.powerups_collected = 0     # total power-ups picked up

        # ── Focus Flow Mode ──────────────────────────────────────────────
        # The Focus Gauge fills as the player types correctly without errors.
        # At 100% it activates Hyper Mode for 6 seconds (see record_correct_char).
        self.focus_charge = 0.0         # current charge level (0.0 – 100.0)
        self.focus_active = False       # True while Hyper Mode is running
        self.focus_timer = 0.0          # ms remaining in active Hyper Mode

    def start(self):
        """Mark the start of gameplay for WPM calculation."""
        self.start_time = time.time()

    def get_elapsed_seconds(self) -> float:
        """Get seconds since game started."""
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time

    def get_elapsed_minutes(self) -> float:
        """
        Get minutes since game started.
        Clamped to a minimum of 1/60 sec to prevent division-by-zero
        on the very first frames before enough time has passed.
        """
        return max(self.get_elapsed_seconds() / 60.0, 1.0 / 60.0)

    def get_wpm(self) -> float:
        """
        Calculate Words Per Minute.
        Uses the standard definition: 1 word = 5 keystrokes.
        Only correct characters count toward WPM.
        """
        if self.correct_chars == 0:
            return 0.0
        words = self.correct_chars / 5.0   # convert chars → "standard words"
        return round(words / self.get_elapsed_minutes(), 1)

    def get_accuracy(self) -> float:
        """
        Get accuracy as a percentage (0.0 – 100.0).
        Returns 100.0 if no characters have been typed yet.
        """
        total = self.total_chars_typed
        if total == 0:
            return 100.0
        return round((self.correct_chars / total) * 100.0, 1)

    def record_correct_char(self):
        """
        Record a correctly typed character.
        Also charges the Focus Gauge by 1.5%.
        When the gauge reaches 100%, Focus Flow (Hyper Mode) activates for 6 seconds.
        Charging is paused while Hyper Mode is already active.
        """
        self.total_chars_typed += 1
        self.correct_chars += 1

        # Only charge while not already in Focus Flow
        if not self.focus_active:
            self.focus_charge = min(100.0, self.focus_charge + 1.5)
            if self.focus_charge >= 100.0:
                self.focus_active = True
                self.focus_timer = 6000.0   # 6 seconds expressed in milliseconds

    def record_wrong_char(self):
        """
        Record an incorrectly typed character.
        Applies a 10% penalty to the Focus Gauge.
        Penalty is ignored while Hyper Mode is active (can't cancel an active run).
        """
        self.total_chars_typed += 1
        self.wrong_chars += 1

        if not self.focus_active:
            self.focus_charge = max(0.0, self.focus_charge - 10.0)

    def record_word_complete(self, score_earned: int):
        """
        Record a completed word and update the combo streak.
        If Focus Flow (Hyper Mode) is active, the score is doubled on top of
        the regular combo multiplier (i.e. up to 2× the combo amount).
        Returns the actual score added.
        """
        self.words_completed += 1
        self.combo += 1
        self.max_combo = max(self.max_combo, self.combo)
        self._update_multiplier()

        # Double the effective multiplier during Focus Flow
        actual_mult = self.multiplier * 2 if self.focus_active else self.multiplier
        actual_score = int(score_earned * actual_mult)
        self.score += actual_score
        return actual_score

    def record_enemy_defeated(self, is_boss: bool = False):
        """Record an enemy kill, tracking boss kills separately."""
        self.enemies_defeated += 1
        if is_boss:
            self.boss_kills += 1

    def break_combo(self):
        """
        Reset the combo streak and multiplier back to ×1.
        Called whenever the player makes a typing mistake.
        """
        self.combo = 0
        self.multiplier = 1

    def _update_multiplier(self):
        """
        Update the score multiplier based on current combo streak.
        Thresholds are defined in settings.COMBO_THRESHOLDS:
            2 streak → ×2,  5 → ×3,  10 → ×5,  20 → ×10
        """
        self.multiplier = 1  # start from base
        for threshold, mult in sorted(COMBO_THRESHOLDS.items()):
            if self.combo >= threshold:
                self.multiplier = mult  # keep upgrading as thresholds are met
            else:
                break  # thresholds are sorted ascending, so stop early

    def add_raw_score(self, points: int):
        """Add score directly without applying the multiplier (e.g. time bonuses)."""
        self.score += points

    def record_wave_complete(self):
        """Record that a full wave of enemies has been cleared."""
        self.waves_survived += 1

    def record_powerup(self):
        """Record a power-up pickup event."""
        self.powerups_collected += 1

    def get_summary(self) -> dict:
        """
        Return a snapshot of all stats for use on the game-over screen
        and for persistence in the scores JSON file.
        """
        return {
            "score":             self.score,
            "wpm":               self.get_wpm(),
            "accuracy":          self.get_accuracy(),
            "max_combo":         self.max_combo,
            "enemies_defeated":  self.enemies_defeated,
            "boss_kills":        self.boss_kills,
            "words_completed":   self.words_completed,
            "correct_chars":     self.correct_chars,
            "wrong_chars":       self.wrong_chars,
            "time_played":       round(self.get_elapsed_seconds(), 1),
            "waves_survived":    self.waves_survived,
            "powerups_collected": self.powerups_collected,
        }
