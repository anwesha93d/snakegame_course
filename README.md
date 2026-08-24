# 🐍 CyberSnake - Modern Python Snake Game

A sleek, retro-cyberpunk edition of the classic Snake game built in Python.

Powered by Python's standard `turtle` graphics library with **zero external dependencies** (`pip` is not required).

---

## ✨ Visual & Gameplay Features

- 🎨 **Cyberpunk Neon Aesthetics**: Dark arena with neon borders and subtle grid lines.
- 👀 **Directional Snake Eyes**: The snake head has animated eyes that look in the direction you are steering.
- 🌈 **Gradient Body**: Snake body segments dynamically transition through a smooth emerald-to-cyan gradient.
- 🍎 **Pulsing Glowing Food**: Food items have an animated glowing halo.
- 🌟 **Golden Bonus Food**: Special golden stars spawn periodically with extra points (`+50 ★`) and a countdown timer.
- ✨ **Particle & Floating Popups**: Enjoy floating score badges (`+10`, `+50`) and colorful particle burst explosions upon eating food.
- 📊 **Modern Cyber HUD**: Real-time Score, Session High Score, and Bonus Timer.
- 🎮 **Start, Pause & Game Over Screens**: Easy flow with instant spacebar controls.

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.6 or higher installed on your computer.

### 2. Run the Game
```bash
python3 snake.py
```

---

## 🎮 Controls

| Action | Primary Key | Secondary Key |
| :--- | :--- | :--- |
| **Move Up** | `↑` (Up Arrow) | `W` |
| **Move Down** | `↓` (Down Arrow) | `S` |
| **Move Left** | `←` (Left Arrow) | `A` |
| **Move Right** | `→` (Right Arrow) | `D` |
| **Start / Pause / Resume** | `Space` | `P` |
| **Restart Game** | `Space` *(on Game Over)* | `R` |

---

## 📜 Scoring & Rules

| Item | Points | Effect |
| :--- | :--- | :--- |
| **Ruby Apple** 🍎 | `+10` | Snake grows +1 segment; game slightly speeds up |
| **Golden Star** 🌟 | `+50` | Bonus fruit that appears for a limited time! |

> [!WARNING]
> Hitting the outer neon border or your own tail triggers Game Over.

---

## ⚙️ Customization

Customize game colors, speeds, and dimensions in [`snake.py`](file:///Users/anweshadas/Desktop/AntiGravity%20course/snake.py):

```python
# Screen dimensions
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
PLAY_AREA_SIZE = 540

# Colors (Cyberpunk Palette)
COLOR_BG = "#0c0e17"
COLOR_ARENA_BG = "#131728"
COLOR_BORDER = "#00f2fe"
COLOR_HEAD = "#00ff87"
COLOR_FOOD = "#ff2a6d"
COLOR_BONUS_FOOD = "#ffd700"
```
