# Project Context: CyberSnake Deluxe

## 🎮 Project Overview
**CyberSnake Deluxe** is a feature-rich, retro-cyberpunk edition of the classic Snake game built in Python. It features 800x600 resolution, vector graphics, smooth 60 FPS animation, dynamic color-morphing snake palettes on eating circular pies, manual 5-level speed controls, particle explosions, floating score popups, dynamic directional eyes, cyber power-ups (Phase Shield, Matrix Slow-Mo, Tail Trimmer, Super Star, Cyber Magnet), combo streak multipliers, theme-morphing level progression, persistent game-over screens, and screen shake.

---

## 🏗️ Core Architecture & Conventions

- **Language & Runtime**: Python 3.6+
- **Entry Point**: `snake.py`
- **Resolution**: `800x600` (`PLAY_AREA_WIDTH = 720`, `PLAY_AREA_HEIGHT = 460`, `GRID_SIZE = 20`)
- **Rendering Engine**: Python standard library `turtle` module utilizing double-buffered manual frame rendering (`turtle.tracer(0)` + `screen.update()`).
- **Dependency Policy**: **Zero third-party dependencies**. Use Python standard library only (`turtle`, `time`, `random`, `math`). Never add `requirements.txt` or third-party packages (e.g., `pygame`) unless explicitly requested.

---

## 🧩 Key Components & Systems

1. **`SnakeGame` (Main Engine)**:
   - Manages game state machine: `START`, `PLAYING`, `PAUSED`, `GAMEOVER`.
   - Grid math and coordinate transformations (`GRID_SIZE = 20`, `PLAY_AREA_WIDTH = 720`, `PLAY_AREA_HEIGHT = 460`).
   - Movement steering, body interpolation, collision detection (wall and self-tail).
   - HUD rendering (Score, High Score, Level/Theme, Speed Indicator, Snake Color, Active Powerup duration bar).

2. **Color-Morphing Snake**:
   - Snake dynamically transforms through vibrant neon color palettes (Neon Green, Electric Cyan, Hot Magenta, Solar Gold, Ultra Violet, Plasma Flame, Arctic Mint, Radioactive Lime) every time it eats a circular pie.

3. **Speed Control System**:
   - Real-time speed presets (1: Relaxed, 2: Normal, 3: Fast, 4: Turbo, 5: Hyper) controllable via keys `1`-`5`, `+`/`-`, or `[`/`]`.

4. **Power-Up System**:
   - `shield` (Phase Shield 🛡️): Wrap through arena walls and gain immunity to self-tail collision.
   - `slow` (Matrix Slow-Mo ⏱️): Bullet-time precision speed mode.
   - `shrink` (Tail Trimmer ✂️): Instantly trims snake tail by 50% when crowded.
   - `star` (Super Star 🌟): Instant +60 points and mega combo surge.
   - `magnet` (Cyber Magnet 🧲): Automatically pulls nearby circular pies closer.

5. **Combo Streak System**:
   - Rapidly consuming food builds a combo multiplier (x1 up to x5+).
   - Dynamic floating combo popups and bonus score calculations.

6. **Input Handler**:
   - Dual control bindings:
     - **Directional**: Arrow Keys (`↑`, `↓`, `←`, `→`) and WASD (`W`, `A`, `S`, `D`).
     - **Speed**: `1`, `2`, `3`, `4`, `5` and `+`/`-`, `[`/`]`.
     - **Actions**: `Space` (Start / Pause / Resume / Restart) and `P` (Pause), `R` (Restart).


---

## 🛠️ Development & Verification Commands

- **Run Game**:
  ```bash
  python3 snake.py
  ```
- **Syntax Check / Compilation**:
  ```bash
  python3 -m py_compile snake.py
  ```

---

## 🎨 Design & Styling Guidelines

- **Theme**: Cyberpunk / Neon Dark.
- **Palette Constants**:
  - Background: `#0c0e17`
  - Arena Background: Theme-based (`#131728`, `#101e17`, `#1c1224`, `#171228`, `#221a10`)
  - Border Accents: `#00f2fe`, `#39ff14`, `#ff007f`, `#b026ff`, `#ffd700`
  - Snake Head: `#00ff87` (Shield: `#b026ff`)
  - Food: `#ff2a6d` (Ruby)
- **Timing & Performance**: Maintain responsive game loop without blocking sleeps; use coordinate bounds matching `PLAY_AREA_SIZE`.

