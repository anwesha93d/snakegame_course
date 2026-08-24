# Project Guidelines: CyberSnake Deluxe

Single-file Python Snake game with retro-cyberpunk vector graphics. `snake.py` is the entire app — no frameworks, no test suite, no CI.

## Commands
- **Run**: `python3 snake.py` (opens a GUI window; requires a display/Tk — fails headless)
- **Verify**: `python3 -m py_compile snake.py` — the only automated check available. There are no tests, lint, or formatter configs.

## Hard Constraints
- **Standard library only** (`turtle`, `time`, `random`, `math`). Never add third-party packages or a `requirements.txt` unless explicitly requested.
- Rendering uses manual double-buffering: `screen.tracer(0)` with one `screen.update()` per loop pass. Always create turtles with `penup()` + `speed(0)`; do not add blocking work to the main loop beyond the frame `time.sleep`.
- Python 3.6+ compatible syntax.

## Gotchas
- The arena is shifted down by `arena_offset_y = -30` (in `SnakeGame.__init__`) to fit the HUD. All gameplay Y coordinates — food/bonus/powerup spawning, wall-collision bounds — must include this offset, or entities misalign with the border and grid.
- Positions are grid-aligned to `GRID_SIZE = 20`; keep any new spawn/movement logic on this lattice.
- Dead/hidden turtles are parked offscreen at `(2000, 2000)` in addition to `hideturtle()` — follow this pattern for new entities.
- Body gradient endpoints are generated from `LEVEL_THEMES` inside `_setup_gradient_segments`.
- Window close raises `turtle.Terminator`, which is caught in `SnakeGame.run()`; new top-level game code must live inside that loop or handle it too.

## Architecture
- `SnakeGame.run()` is the main loop: `screen.update()` → effect updates → state-gated logic → paced sleep. State machine: `START`, `PLAYING`, `PAUSED`, `GAMEOVER` (string field `self.state`).
- Effect systems: `Particle` (bursts/death explosion), `PopupText` (+10/combo/powerup floaters), screen shake; each `update()` returns `False` when expired and callers filter the lists.
- Power-ups: `Phase Shield`, `Matrix Slow-Mo`, `Tail Trimmer`, `Super Star`, `Cyber Magnet`.
- Keys (bound in `_bind_keys`): Arrows/WASD steer, Space start/pause/resume/restart, `P` pause toggle, `R` reset.

## Related Files
- `Gemini.md` mirrors these guidelines plus the full color palette; keep the two in sync when conventions change.

