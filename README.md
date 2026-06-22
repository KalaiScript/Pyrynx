# 🎮 Typing Takedown

**A Python-based typing combat game where you defeat enemies by typing Python syntax, terminal commands, and tech keywords.**

Built with Pygame-CE — featuring wave-based combat, power-ups, achievements, enemy variety, real-time input validation, combo systems, particle effects, and WPM/accuracy analytics.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Pygame-CE](https://img.shields.io/badge/Pygame--CE-2.5+-green?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ⚡ Features

- **6 Game Modes**: Classic Survival, Time Attack, Boss Rush, Debug Mode, Command Line, Interview Mode
- **Wave System**: Structured waves with rest periods, progressive difficulty scaling
- **Power-Up System**: 5 collectible power-ups — Shield, Health, Freeze, Score Boost, Nuke
- **Enemy Variety**: 4 enemy types — Normal, Fast (1.5x speed), Armored (2 HP), Splitter (splits on defeat)
- **12 Achievements**: Unlockable milestones with persistent tracking and toast notifications
- **How To Play**: 5-page interactive tutorial covering controls, scoring, power-ups, and modes
- **Real-time Input Matching**: Character-by-character feedback with green/red highlighting
- **Python-Themed Content**: Type `print()`, `for i in range(10):`, `pip install pygame`, and more
- **Combo & Multiplier System**: Chain correct words for score multipliers up to x10
- **Live Stats**: WPM, accuracy, combo streak tracked in real-time
- **Particle Effects**: Explosions, matrix rain, floating score text
- **Procedural Sound**: 15 retro synth sound effects — no external audio files needed
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

## 🔋 Power-Ups

| Power-Up | Effect | Visual |
|----------|--------|--------|
| **Shield** | Blocks the next damage hit | Cyan glow |
| **+HP** | Restores 1 health point | Green glow |
| **Freeze** | Slows all enemies for 5 seconds | Ice blue glow |
| **2x Score** | Double points for 10 seconds | Gold glow |
| **Nuke** | Destroys all enemies on screen | Magenta glow |

---

## 👾 Enemy Types

| Type | Behavior | Visual |
|------|----------|--------|
| **Normal** | Standard speed, 1 HP | Default border |
| **Fast** | 1.5x speed | Orange border + speed lines |
| **Armored** | 2 HP — type the word twice | Thick grey border |
| **Splitter** | Splits into 2 smaller enemies on defeat | Green glow + split dots |
| **Boss** | Long code, 3 HP, slow | Purple glow |

---

## 🏆 Achievements (12 Total)

| Achievement | Condition |
|-------------|-----------|
| First Blood | Defeat your first enemy |
| Speed Demon | Reach 80+ WPM |
| Perfectionist | 100% accuracy with 10+ words |
| Combo Master | Achieve x10 combo multiplier |
| Boss Slayer | Defeat 5 bosses total |
| Centurion | Score 10,000+ in one game |
| Survivor | Survive 10 waves |
| Debugger | Complete a Debug Mode game |
| Terminal Hacker | Complete a Command Line game |
| Polyglot | Play all 6 game modes |
| Unstoppable | Defeat 50 enemies in one game |
| Marathon | Play for 5+ minutes in one game |

---

## 🕹️ Controls

| Key | Action |
|-----|--------|
| ↑/↓ | Navigate menus |
| ←/→ | Switch pages/tabs |
| Enter | Select |
| ESC | Pause / Back |
| A-Z, 0-9, symbols | Type to attack enemies |

---

## 🧪 Testing

The game includes an automated headless verification test suite that validates core combat mechanics (including normal/armored/boss HP hits, splitter split mechanics and child scaling, combo systems, and wave transitions).

To run the automated tests in headless mode (no window display or audio output required):
```bash
python scratch/verify_gameplay.py
```

---

## 📁 Project Structure

```
typing_takedown/
├── main.py              # Entry point
├── game.py              # Core game loop & state machine
├── player.py            # Player class (health, power-up timers, rendering)
├── enemy.py             # Enemy class (4 types, movement, targeting)
├── projectile.py        # Attack effect animations
├── particle.py          # Particle system (explosions, matrix rain)
├── powerup.py           # Power-up system (5 types, drops, collection)
├── achievements.py      # Achievement definitions & persistence
├── text_bank.py         # Python-themed word database
├── ui.py                # Menus, HUD, tutorial, achievements screen
├── stats.py             # WPM, accuracy, combo, wave tracking
├── scores.py            # High score JSON persistence
├── settings.py          # Constants, colors, difficulty config
├── sound_manager.py     # 15 procedural sound effects
├── requirements.txt     # Dependencies
├── scores.json          # Auto-generated high scores
├── achievements.json    # Auto-generated achievement progress
└── scratch/             # Helper scripts
    └── verify_gameplay.py # Headless automated gameplay tests
```

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Pygame-CE 2.5+** — Game engine, rendering, input handling
- **NumPy** — Procedural sound wave generation
- **JSON** — High score & achievement persistence

---

## 📊 Scoring System

- **10 points** per correct character
- **50 bonus** per word completed
- **200 bonus** per boss defeated
- **Combo multipliers**: x2 (2 streak), x3 (5), x5 (10), x10 (20)
- **Score Boost power-up**: Doubles all points for 10 seconds

---

## 📄 License

MIT License — feel free to use, modify, and share.
