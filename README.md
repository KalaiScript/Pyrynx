# 🎮 Typing Takedown

**A Python-based typing combat game where you defeat enemies by typing Python syntax, terminal commands, and tech keywords.**

Built with Pygame-CE — featuring wave-based combat, power-ups, achievements, enemy variety, real-time input validation, combo systems, particle effects, WPM/accuracy analytics, and two signature high-skill mechanics: **Focus Flow** and **Ghost Word Revival**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Pygame-CE](https://img.shields.io/badge/Pygame--CE-2.5+-green?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ⚡ Features

- **6 Game Modes**: Classic Survival, Time Attack, Boss Rush, Debug Mode, Command Line, Interview Mode
- **Wave System**: Structured waves with rest periods and progressive difficulty scaling
- **Power-Up System**: 5 collectible power-ups — Shield, Health, Freeze, Score Boost, Nuke
- **Enemy Variety**: 4 enemy types — Normal, Fast, Armored (2 HP), Splitter
- **👻 Ghost Word Revival**: Drop to 1 HP and a ghost word challenge appears — type it within 5 seconds to survive
- **⚡ Focus Flow (Hyper Mode)**: Build a typing streak to charge a gauge — at 100%, activate 2× points + chain lightning for 6 seconds
- **12 Achievements**: Unlockable milestones with persistent tracking and toast notifications
- **5-Page Tutorial**: Interactive walkthrough covering controls, scoring, power-ups, and modes
- **Real-time Input Matching**: Character-by-character feedback with green/red highlighting
- **Python-Themed Content**: Type `print()`, `for i in range(10):`, `pip install pygame`, and more
- **Combo & Multiplier System**: Chain correct words for score multipliers up to x10
- **Live Stats**: WPM, accuracy, combo streak tracked in real-time
- **Particle Effects**: Explosions, matrix rain, floating score text, chain lightning arcs
- **Procedural Sound**: 17 retro synth sound effects — no external audio files needed
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

## ✨ Special Mechanics

### ⚡ Focus Flow (Hyper Mode)

Build your typing accuracy to charge the **Focus Gauge** below the input box:

| State | Effect |
|-------|--------|
| Correct keystroke | +1.5% charge |
| Typo | −10% charge |
| Idle (no typing) | −5% per second |
| **100% charged** | **Focus Flow activates for 6 seconds** |

**While Focus Flow is active:**
- **2× Points** on all word completions (stacks with Score Boost for 4×)
- **Chain Lightning** — completing a word fires a jagged arc to another enemy on screen
- **Matrix rain** background doubles in speed
- Pulsing cyan border vignette frames the screen

---

### 👻 Ghost Word Revival

When you drop to **1 HP** for the first time in a session, enemies freeze and a ghostly challenge card appears:

- Type the displayed word correctly within **5 seconds** to earn **+1 HP** and continue
- The countdown clock shifts from **cyan → yellow → red** as time runs out
- A wrong character **resets** your typed progress
- On success: particle burst + `REVIVED!` floating text + triumph sound
- On failure: instant game over
- **One-time use only** per game session

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
| **Fast** | 1.5× speed | Orange border |
| **Armored** | 2 HP — type the word twice | Thick grey border |
| **Splitter** | Splits into 2 smaller enemies on defeat | Green glow |
| **Boss** | Long code snippet, 3 HP | Purple glow |

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
| A–Z, 0–9, symbols | Type to attack enemies |

---

## 📊 Scoring System

| Action | Points |
|--------|--------|
| Correct character | +10 pts |
| Word completed | +50 bonus |
| Boss defeated | +200 bonus |
| Combo x2 (2 streak) | ×2 multiplier |
| Combo x3 (5 streak) | ×3 multiplier |
| Combo x5 (10 streak) | ×5 multiplier |
| Combo x10 (20 streak) | ×10 multiplier |
| Score Boost power-up | ×2 all points (10 sec) |
| Focus Flow active | ×2 all points (stacks) |

---

## 📁 Project Structure

```
typing_takedown/
├── main.py              # Entry point
├── game.py              # Core game loop & state machine
├── player.py            # Player class (health, power-up timers, rendering)
├── enemy.py             # Enemy class (4 types, movement, targeting)
├── projectile.py        # Attack effect animations
├── particle.py          # Particles, matrix rain, lightning arcs
├── powerup.py           # Power-up system (5 types, drops, collection)
├── achievements.py      # Achievement definitions & persistence
├── text_bank.py         # Python-themed word database
├── ui.py                # Menus, HUD, ghost revival overlay, tutorial
├── stats.py             # WPM, accuracy, combo, focus gauge tracking
├── scores.py            # High score JSON persistence
├── settings.py          # Constants, colors, difficulty config
├── sound_manager.py     # 17 procedural sound effects
├── requirements.txt     # Dependencies
├── scores.json          # Auto-generated high scores
├── achievements.json    # Auto-generated achievement progress
└── scratch/
    └── verify_gameplay.py  # Headless automated test suite (8 tests)
```

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Pygame-CE 2.5+** — Game engine, rendering, input handling
- **NumPy** — Procedural sound wave generation
- **JSON** — High score & achievement persistence

---

## 🧪 Testing

A headless automated test suite covers all core gameplay mechanics:

```bash
./.venv/bin/python scratch/verify_gameplay.py
```

| Test | Coverage |
|------|----------|
| Test 1 | Game initialization & state machine |
| Test 2 | Normal enemy (1 HP) defeat |
| Test 3 | Armored enemy (2 HP) — two-pass defeat |
| Test 4 | Boss enemy (3 HP) — three-pass defeat |
| Test 5 | Splitter split behavior & wave speed scaling |
| Test 6 | Wave completion trigger |
| Test 7 | Focus Flow charging, typo penalty, 2× score, chain lightning |
| Test 8 | Ghost Word Revival — state trigger, success path, one-time use, timer fail |

---

## 📄 License

MIT License — feel free to use, modify, and share.
