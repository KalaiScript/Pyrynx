# 🎮 Typing Takedown

**A Python-based typing combat game where you defeat enemies by typing Python syntax, terminal commands, and tech keywords.**

Built with Pygame — featuring real-time input validation, dynamic enemy spawning, combo systems, particle effects, and WPM/accuracy analytics.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ⚡ Features

- **6 Game Modes**: Classic Survival, Time Attack, Boss Rush, Debug Mode, Command Line, Interview Mode
- **Real-time Input Matching**: Character-by-character feedback with green/red highlighting
- **Python-Themed Content**: Type `print()`, `for i in range(10):`, `pip install pygame`, and more
- **Combo & Multiplier System**: Chain correct words for score multipliers up to x10
- **Live Stats**: WPM, accuracy, combo streak tracked in real-time
- **Particle Effects**: Explosions, matrix rain, floating score text
- **Procedural Sound**: Retro synth sound effects — no external audio files needed
- **Difficulty Scaling**: Enemies get faster and more complex over time
- **Boss Enemies**: Longer Python snippets with multi-hit HP
- **High Score Persistence**: Top 10 scores per mode saved to JSON
- **Cyberpunk Aesthetic**: CRT scanlines, neon glow effects, terminal-style player

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/typing-takedown.git
cd typing-takedown

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the game!
python main.py
```

---

## 🎯 Game Modes

| Mode | Description |
|------|-------------|
| **Classic Survival** | Endless waves — survive as long as you can |
| **Time Attack** | Maximize score in 90–120 seconds |
| **Boss Rush** | Fewer enemies, longer Python snippets |
| **Debug Mode** | Fix broken Python code to defeat enemies |
| **Command Line** | Terminal commands: `git`, `pip`, `cd`, `ssh` |
| **Interview Mode** | DSA terms and Python concepts |

---

## 🕹️ Controls

| Key | Action |
|-----|--------|
| ↑/↓ | Navigate menus |
| Enter | Select |
| ESC | Pause / Back |
| A-Z, 0-9, symbols | Type to attack enemies |

---

## 📁 Project Structure

```
typing_takedown/
├── main.py              # Entry point
├── game.py              # Core game loop & state machine
├── player.py            # Player class (health, combo, rendering)
├── enemy.py             # Enemy class (text, movement, targeting)
├── projectile.py        # Attack effect animations
├── particle.py          # Particle system (explosions, matrix rain)
├── text_bank.py         # Python-themed word database
├── ui.py                # Menus, HUD, game over screen
├── stats.py             # WPM, accuracy, combo tracking
├── scores.py            # High score JSON persistence
├── settings.py          # Constants, colors, difficulty config
├── sound_manager.py     # Procedural sound effects
├── requirements.txt     # Dependencies
└── scores.json          # Auto-generated high scores
```

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Pygame 2.5+** — Game engine, rendering, input handling
- **NumPy** — Procedural sound wave generation
- **JSON** — High score persistence

---

## 📊 Scoring System

- **10 points** per correct character
- **50 bonus** per word completed
- **200 bonus** per boss defeated
- **Combo multipliers**: x2 (2 streak), x3 (5), x5 (10), x10 (20)

---

## 📄 License

MIT License — feel free to use, modify, and share.
