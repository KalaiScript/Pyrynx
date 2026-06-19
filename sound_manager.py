"""
Typing Takedown — Sound Manager
Procedurally generated sound effects using numpy + pygame.mixer.
"""

import pygame
import numpy as np
import math


class SoundManager:
    """Generates and plays sound effects procedurally."""

    def __init__(self):
        self.enabled = True
        self.sounds = {}
        self._initialized = False

    def init(self):
        """Initialize and generate all sounds. Call after pygame.mixer.init()."""
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
            self._generate_all()
            self._initialized = True
        except Exception:
            self.enabled = False

    def _make_sound(self, frequency, duration_ms, wave="sine",
                    fade_out=True, volume=0.3):
        """Generate a pygame Sound from a waveform."""
        sample_rate = 44100
        n_samples = int(sample_rate * duration_ms / 1000.0)
        t = np.linspace(0, duration_ms / 1000.0, n_samples, dtype=np.float32)

        if wave == "sine":
            samples = np.sin(2 * np.pi * frequency * t)
        elif wave == "square":
            samples = np.sign(np.sin(2 * np.pi * frequency * t))
        elif wave == "saw":
            samples = 2 * (t * frequency - np.floor(0.5 + t * frequency))
        else:
            samples = np.sin(2 * np.pi * frequency * t)

        if fade_out:
            envelope = np.linspace(1.0, 0.0, n_samples, dtype=np.float32)
            samples *= envelope

        samples = (samples * volume * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(samples)
        return sound

    def _make_noise_burst(self, duration_ms, volume=0.15):
        """Generate a noise burst sound."""
        sample_rate = 44100
        n_samples = int(sample_rate * duration_ms / 1000.0)
        samples = np.random.uniform(-1, 1, n_samples).astype(np.float32)
        envelope = np.linspace(1.0, 0.0, n_samples, dtype=np.float32)
        samples *= envelope * volume
        samples = (samples * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(samples)

    def _make_multi_tone(self, freqs_durations, wave="sine", volume=0.3):
        """Generate a multi-tone sound (sequence of frequencies)."""
        sample_rate = 44100
        all_samples = []
        for freq, dur_ms in freqs_durations:
            n = int(sample_rate * dur_ms / 1000.0)
            t = np.linspace(0, dur_ms / 1000.0, n, dtype=np.float32)
            if wave == "sine":
                s = np.sin(2 * np.pi * freq * t)
            else:
                s = np.sign(np.sin(2 * np.pi * freq * t))
            env = np.linspace(1.0, 0.3, n, dtype=np.float32)
            all_samples.append(s * env)
        combined = np.concatenate(all_samples)
        combined = (combined * volume * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(combined)

    def _generate_all(self):
        """Generate all game sounds."""
        # Key press - soft click
        self.sounds["keypress"] = self._make_sound(800, 30, "square", volume=0.08)
        # Correct character
        self.sounds["correct"] = self._make_sound(1200, 50, "sine", volume=0.12)
        # Wrong character
        self.sounds["wrong"] = self._make_sound(200, 120, "square", volume=0.15)
        # Word complete
        self.sounds["complete"] = self._make_multi_tone(
            [(880, 60), (1100, 60), (1320, 80)], "sine", volume=0.2
        )
        # Enemy destroyed
        self.sounds["destroy"] = self._make_multi_tone(
            [(600, 40), (900, 40), (1200, 60), (1600, 80)], "sine", volume=0.25
        )
        # Combo milestone
        self.sounds["combo"] = self._make_multi_tone(
            [(660, 50), (880, 50), (1100, 50), (1320, 70)], "sine", volume=0.2
        )
        # Damage taken
        self.sounds["damage"] = self._make_sound(150, 200, "saw", volume=0.25)
        # Game over
        self.sounds["gameover"] = self._make_multi_tone(
            [(440, 200), (350, 200), (280, 300), (220, 400)], "sine", volume=0.3
        )
        # Boss appear
        self.sounds["boss"] = self._make_multi_tone(
            [(200, 150), (180, 150), (160, 200)], "square", volume=0.2
        )
        # Menu select
        self.sounds["select"] = self._make_sound(1000, 60, "sine", volume=0.15)
        # Menu navigate
        self.sounds["navigate"] = self._make_sound(600, 40, "sine", volume=0.1)

    def play(self, name: str):
        """Play a named sound effect."""
        if not self.enabled or not self._initialized:
            return
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def toggle(self):
        """Toggle sound on/off."""
        self.enabled = not self.enabled
