"""
🐍 CyberSnake Deluxe - Enhanced Retro-Cyberpunk Edition
Features:
- Screen Dimensions: 800x600 with spacious widescreen arena
- Dynamic Color-Morphing Snake: Changes vibrant neon color theme every time it eats the circular pie!
- Interactive Snake Speed Control: Select speeds 1-5 or use +/- in real-time
- Dynamic Cyber Power-ups:
  🛡️ Phase Shield: Wall wrap-around & tail invulnerability
  ⏱️ Matrix Slow-Mo: Bullet-time precision mode
  ✂️ Tail Trimmer: Instantly trims tail when crowded
  🌟 Super Star: Massive score burst
  🧲 Cyber Magnet: Pulls nearby food closer
- Combo Streak System with scoring multipliers & floating announcers
- Multi-Level Progression with dynamic cyberpunk arena theme color shifts
- Persistent Game Over screen with comprehensive stats breakdown
- Juiced Visuals: Pulsing circular pie, directional snake eyes, particle bursts, screen shake
"""

import math
import random
import time
import turtle

# --- Screen & Arena Configuration ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAY_AREA_WIDTH = 720
PLAY_AREA_HEIGHT = 480
GRID_SIZE = 20

# --- Speed Presets (Level, Label, Delay in seconds) ---
SPEED_PRESETS = {
    1: {"name": "RELAXED", "delay": 0.110},
    2: {"name": "NORMAL", "delay": 0.080},
    3: {"name": "FAST", "delay": 0.055},
    4: {"name": "TURBO", "delay": 0.038},
    5: {"name": "HYPER", "delay": 0.024},
}
DEFAULT_SPEED_LEVEL = 2

# --- Vibrant Snake Color Themes (Morphs each time circular pie is eaten) ---
SNAKE_COLOR_THEMES = [
    {
        "name": "NEON GREEN",
        "head": "#00ff87",
        "body_start": (0x00, 0xFF, 0x87),
        "body_end": (0x00, 0x77, 0xB6),
        "sparkle": "#00ff87",
    },
    {
        "name": "ELECTRIC CYAN",
        "head": "#00f2fe",
        "body_start": (0x00, 0xF2, 0xFE),
        "body_end": (0x4F, 0x46, 0xE5),
        "sparkle": "#00f2fe",
    },
    {
        "name": "HOT MAGENTA",
        "head": "#ff007f",
        "body_start": (0xFF, 0x00, 0x7F),
        "body_end": (0x79, 0x28, 0xCA),
        "sparkle": "#ff007f",
    },
    {
        "name": "SOLAR GOLD",
        "head": "#ffd700",
        "body_start": (0xFF, 0xD7, 0x00),
        "body_end": (0xFF, 0x57, 0x22),
        "sparkle": "#ffd700",
    },
    {
        "name": "ULTRA VIOLET",
        "head": "#b026ff",
        "body_start": (0xB0, 0x26, 0xFF),
        "body_end": (0x00, 0xD2, 0xFF),
        "sparkle": "#b026ff",
    },
    {
        "name": "PLASMA FLAME",
        "head": "#ff3b30",
        "body_start": (0xFF, 0x3B, 0x30),
        "body_end": (0xFF, 0x95, 0x00),
        "sparkle": "#ff3b30",
    },
    {
        "name": "ARCTIC MINT",
        "head": "#00f5d4",
        "body_start": (0x00, 0xF5, 0xD4),
        "body_end": (0x00, 0xBB, 0xF9),
        "sparkle": "#00f5d4",
    },
    {
        "name": "RADIOACTIVE LIME",
        "head": "#39ff14",
        "body_start": (0x39, 0xFF, 0x14),
        "body_end": (0xCC, 0xFF, 0x00),
        "sparkle": "#39ff14",
    },
]

# --- Cyberpunk Arena Themes per Level ---
LEVEL_THEMES = [
    {
        "name": "CYBER CITY",
        "border": "#00f2fe",
        "shadow": "#102a45",
        "accent": "#05d9e8",
        "bg_inner": "#131728",
    },
    {
        "name": "NEON MATRIX",
        "border": "#39ff14",
        "shadow": "#12381a",
        "accent": "#00ff87",
        "bg_inner": "#101e17",
    },
    {
        "name": "SYNTHWAVE",
        "border": "#ff007f",
        "shadow": "#3b0e2b",
        "accent": "#ff2a6d",
        "bg_inner": "#1c1224",
    },
    {
        "name": "VAPORWAVE",
        "border": "#b026ff",
        "shadow": "#2c1245",
        "accent": "#d946ef",
        "bg_inner": "#171228",
    },
    {
        "name": "HYPERDRIVE",
        "border": "#ffd700",
        "shadow": "#3a300a",
        "accent": "#ff8800",
        "bg_inner": "#221a10",
    },
]

# --- Static Color Constants ---
COLOR_BG = "#0c0e17"
COLOR_HEAD_SHIELD = "#b026ff"
COLOR_PUPILS = "#0c0e17"
COLOR_FOOD_CORE = "#ff2a6d"
COLOR_FOOD_PIE_CRUST = "#ffd700"
COLOR_FOOD_GLOW = "#ff7597"
COLOR_TEXT = "#ffffff"
COLOR_MUTED = "#8b9bb4"

# Power-up definitions (Type, Color, Icon Label, Duration Frames)
POWERUP_TYPES = [
    {"type": "shield", "color": "#b026ff", "name": "PHASE SHIELD 🛡️", "duration": 110},
    {"type": "slow", "color": "#00f2fe", "name": "MATRIX SLOW-MO ⏱️", "duration": 90},
    {"type": "shrink", "color": "#ff6b35", "name": "TAIL TRIMMER ✂️", "duration": 0},
    {"type": "star", "color": "#ffd700", "name": "SUPER STAR 🌟", "duration": 0},
    {"type": "magnet", "color": "#ff007f", "name": "CYBER MAGNET 🧲", "duration": 100},
]


class Particle:
    """A floating particle for eating effects, explosions, and powerup sparkles."""
    def __init__(self, x, y, color, speed_range=(3, 8), life=None, size=0.3):
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.shape("circle")
        self.t.shapesize(size, size)
        self.t.color(color)
        self.t.penup()
        self.t.goto(x, y)
        angle = random.uniform(0, 2 * math.pi)
        spd = random.uniform(speed_range[0], speed_range[1])
        self.dx = math.cos(angle) * spd
        self.dy = math.sin(angle) * spd
        self.life = life if life is not None else random.randint(6, 12)

    def update(self):
        self.t.setx(self.t.xcor() + self.dx)
        self.t.sety(self.t.ycor() + self.dy)
        self.dx *= 0.94  # Slight drag
        self.dy *= 0.94
        self.life -= 1
        if self.life <= 0:
            self.t.hideturtle()
            self.t.goto(2000, 2000)
            return False
        return True


class PopupText:
    """A floating animated score & combo text popup."""
    def __init__(self, x, y, text, color, font_size=11, life=14):
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.hideturtle()
        self.t.color(color)
        self.t.penup()
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size
        self.life = life

    def update(self):
        self.y += 2.2
        self.life -= 1
        self.t.clear()
        if self.life > 0:
            self.t.goto(self.x, self.y)
            self.t.write(self.text, align="center", font=("Arial", self.font_size, "bold"))
            return True
        return False


class SnakeGame:
    def __init__(self):
        # 1. Screen Setup (800x600)
        self.screen = turtle.Screen()
        self.screen.title("🐍 CyberSnake Deluxe - 800x600 Retro Cyberpunk")
        self.screen.bgcolor(COLOR_BG)
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.tracer(0)

        # 2. State & Scores
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.foods_eaten = 0
        self.state = "START"  # "START", "PLAYING", "PAUSED", "GAMEOVER"
        self.segments = []
        self.particles = []
        self.popups = []

        # Speed Control state
        self.speed_level = DEFAULT_SPEED_LEVEL
        self.delay = SPEED_PRESETS[self.speed_level]["delay"]

        # Snake Color Theme State (Cycles on eating circular pie)
        self.color_theme_index = 0

        # Combo system
        self.combo = 0
        self.combo_timer = 0
        self.max_combo = 0

        # Power-up state
        self.active_powerup = None
        self.powerup_timer = 0
        self.spawned_powerup = None
        self.powerup_despawn_timer = 0

        # Screen Shake
        self.shake_frames = 0
        self.shake_magnitude = 0

        # Arena bounds (720x460)
        self.arena_limit_x = PLAY_AREA_WIDTH // 2   # 360
        self.arena_limit_y = PLAY_AREA_HEIGHT // 2  # 230
        self.arena_offset_y = -30                   # Shift arena down slightly to fit top HUD

        # 3. Initialize Drawing Pens & Entities
        self._init_drawers()
        self._init_head()
        self._init_food()
        self._init_powerup_entities()

        # 4. Render Initial Static Background & Arena
        self.draw_static_arena()
        self.update_hud()
        self.show_start_screen()

        # 5. Controls
        self._bind_keys()

    def _get_current_level_theme(self):
        theme_idx = min(self.level - 1, len(LEVEL_THEMES) - 1)
        return LEVEL_THEMES[theme_idx]

    def _get_current_snake_theme(self):
        return SNAKE_COLOR_THEMES[self.color_theme_index % len(SNAKE_COLOR_THEMES)]

    def _init_drawers(self):
        """Creates specialized turtles for arena background, HUD, and overlays."""
        self.bg_pen = turtle.Turtle()
        self.bg_pen.speed(0)
        self.bg_pen.hideturtle()
        self.bg_pen.penup()

        self.hud_pen = turtle.Turtle()
        self.hud_pen.speed(0)
        self.hud_pen.hideturtle()
        self.hud_pen.penup()

        self.overlay_pen = turtle.Turtle()
        self.overlay_pen.speed(0)
        self.overlay_pen.hideturtle()
        self.overlay_pen.penup()

    def _init_head(self):
        """Creates the snake head with custom directional eyes."""
        snake_theme = self._get_current_snake_theme()
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("square")
        self.head.shapesize(0.95, 0.95)
        self.head.color(snake_theme["head"])
        self.head.penup()
        self.head.goto(0, self.arena_offset_y)
        self.head.direction = "stop"

        # Snake eyes
        self.eye_left = turtle.Turtle()
        self.eye_left.speed(0)
        self.eye_left.shape("circle")
        self.eye_left.shapesize(0.22, 0.22)
        self.eye_left.color(COLOR_PUPILS)
        self.eye_left.penup()

        self.eye_right = turtle.Turtle()
        self.eye_right.speed(0)
        self.eye_right.shape("circle")
        self.eye_right.shapesize(0.22, 0.22)
        self.eye_right.color(COLOR_PUPILS)
        self.eye_right.penup()

        self._update_eyes()

    def _init_food(self):
        """Creates the glowing circular pie food (outer aura + crust ring + center ruby pie)."""
        self.food_glow = turtle.Turtle()
        self.food_glow.speed(0)
        self.food_glow.shape("circle")
        self.food_glow.shapesize(1.35, 1.35)
        self.food_glow.color(COLOR_FOOD_GLOW)
        self.food_glow.penup()

        self.food_crust = turtle.Turtle()
        self.food_crust.speed(0)
        self.food_crust.shape("circle")
        self.food_crust.shapesize(1.0, 1.0)
        self.food_crust.color(COLOR_FOOD_PIE_CRUST)
        self.food_crust.penup()

        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.shapesize(0.72, 0.72)
        self.food.color(COLOR_FOOD_CORE)
        self.food.penup()
        self.relocate_food()

    def _init_powerup_entities(self):
        """Creates turtles for temporary special powerup pickups."""
        self.powerup_glow = turtle.Turtle()
        self.powerup_glow.speed(0)
        self.powerup_glow.shape("circle")
        self.powerup_glow.shapesize(1.4, 1.4)
        self.powerup_glow.penup()
        self.powerup_glow.hideturtle()
        self.powerup_glow.goto(2000, 2000)

        self.powerup_core = turtle.Turtle()
        self.powerup_core.speed(0)
        self.powerup_core.shape("square")
        self.powerup_core.shapesize(0.85, 0.85)
        self.powerup_core.penup()
        self.powerup_core.hideturtle()
        self.powerup_core.goto(2000, 2000)

    def draw_static_arena(self, shake_x=0, shake_y=0):
        """Draws the glowing cyberpunk arena backdrop, grid lines, and border with theme colors."""
        self.bg_pen.clear()
        half_w = self.arena_limit_x
        half_h = self.arena_limit_y
        cy = self.arena_offset_y + shake_y
        cx = shake_x

        theme = self._get_current_level_theme()

        # 1. Arena Interior Box
        self.bg_pen.goto(cx - half_w, cy - half_h)
        self.bg_pen.color(theme["bg_inner"])
        self.bg_pen.begin_fill()
        for _ in range(2):
            self.bg_pen.forward(PLAY_AREA_WIDTH)
            self.bg_pen.left(90)
            self.bg_pen.forward(PLAY_AREA_HEIGHT)
            self.bg_pen.left(90)
        self.bg_pen.end_fill()

        # 2. Subtle Grid Matrix
        self.bg_pen.color("#161c2e")
        self.bg_pen.pensize(1)
        for x in range(-half_w + GRID_SIZE, half_w, GRID_SIZE * 2):
            self.bg_pen.penup()
            self.bg_pen.goto(cx + x, cy - half_h)
            self.bg_pen.pendown()
            self.bg_pen.goto(cx + x, cy + half_h)

        for y in range(cy - half_h + GRID_SIZE, cy + half_h, GRID_SIZE * 2):
            self.bg_pen.penup()
            self.bg_pen.goto(cx - half_w, y)
            self.bg_pen.pendown()
            self.bg_pen.goto(cx + half_w, y)

        # 3. Outer Neon Glow Shadow
        self.bg_pen.penup()
        self.bg_pen.goto(cx - half_w - 3, cy - half_h - 3)
        self.bg_pen.color(theme["shadow"])
        self.bg_pen.pensize(5)
        self.bg_pen.pendown()
        for _ in range(2):
            self.bg_pen.forward(PLAY_AREA_WIDTH + 6)
            self.bg_pen.left(90)
            self.bg_pen.forward(PLAY_AREA_HEIGHT + 6)
            self.bg_pen.left(90)

        # 4. Inner Bright Neon Border Frame
        self.bg_pen.penup()
        self.bg_pen.goto(cx - half_w, cy - half_h)
        self.bg_pen.color(theme["border"])
        self.bg_pen.pensize(2)
        self.bg_pen.pendown()
        for _ in range(2):
            self.bg_pen.forward(PLAY_AREA_WIDTH)
            self.bg_pen.left(90)
            self.bg_pen.forward(PLAY_AREA_HEIGHT)
            self.bg_pen.left(90)

        self.bg_pen.penup()

    def update_hud(self):
        """Draws the sleek modern top dashboard with Score, High Score, Speed, Color, and Powerups."""
        self.hud_pen.clear()
        hud_y = (SCREEN_HEIGHT // 2) - 40
        lvl_theme = self._get_current_level_theme()
        snake_theme = self._get_current_snake_theme()
        spd_info = SPEED_PRESETS[self.speed_level]

        # Row 1: Title/Level, Speed Control Indicator, Score, High Score
        # Level Title
        self.hud_pen.goto(-self.arena_limit_x + 10, hud_y + 12)
        self.hud_pen.color(lvl_theme["accent"])
        self.hud_pen.write(f"LVL {self.level}: {lvl_theme['name']}", align="left", font=("Helvetica", 12, "bold"))

        # Speed Control display
        self.hud_pen.goto(-100, hud_y + 12)
        self.hud_pen.color("#00f2fe")
        self.hud_pen.write(f"SPD: {self.speed_level}/5 [{spd_info['name']}] (1-5, +/-)", align="center", font=("Courier", 11, "bold"))

        # Score
        self.hud_pen.goto(150, hud_y + 12)
        self.hud_pen.color(COLOR_TEXT)
        self.hud_pen.write(f"SCORE: {self.score:04d}", align="center", font=("Courier", 13, "bold"))

        # Best / High Score
        self.hud_pen.goto(self.arena_limit_x - 10, hud_y + 12)
        self.hud_pen.color("#ffd700")
        self.hud_pen.write(f"BEST: {self.high_score:04d}", align="right", font=("Courier", 13, "bold"))

        # Row 2: Combo Meter, Snake Color status, and Active Powerup
        sub_y = hud_y - 10
        # Combo Meter
        if self.combo > 1 and self.combo_timer > 0:
            combo_color = "#ff007f" if self.combo >= 4 else "#ffd700"
            self.hud_pen.goto(-self.arena_limit_x + 10, sub_y)
            self.hud_pen.color(combo_color)
            combo_stars = "★" * min(self.combo, 5)
            self.hud_pen.write(f"COMBO x{self.combo} {combo_stars}", align="left", font=("Helvetica", 10, "bold"))
        else:
            self.hud_pen.goto(-self.arena_limit_x + 10, sub_y)
            self.hud_pen.color(COLOR_MUTED)
            self.hud_pen.write(f"SNAKE COLOR: {snake_theme['name']}", align="left", font=("Arial", 9, "bold"))

        # Active Powerup bar
        if self.active_powerup and self.powerup_timer > 0:
            p_color = self.active_powerup["color"]
            p_name = self.active_powerup["name"]
            pct = int((self.powerup_timer / max(self.active_powerup["duration"], 1)) * 10)
            bar = "▮" * pct + "▯" * (10 - pct)
            self.hud_pen.goto(self.arena_limit_x - 10, sub_y)
            self.hud_pen.color(p_color)
            self.hud_pen.write(f"{p_name} [{bar}]", align="right", font=("Courier", 9, "bold"))

    def show_start_screen(self):
        """Displays the stylish start screen with gameplay controls & features guide."""
        self.overlay_pen.clear()
        cy = self.arena_offset_y

        self.overlay_pen.goto(0, cy + 95)
        self.overlay_pen.color(COLOR_HEAD_SHIELD)
        self.overlay_pen.write("🐍 CYBERSNAKE DELUXE 800x600", align="center", font=("Helvetica", 22, "bold"))

        self.overlay_pen.goto(0, cy + 62)
        self.overlay_pen.color("#05d9e8")
        self.overlay_pen.write("EAT CIRCULAR PIES • MORPH SNAKE COLORS • CONTROL REAL-TIME SPEED", align="center", font=("Arial", 10, "bold"))

        features = [
            ("🥧 Circular Pie", "Eats pie to grow & dynamically morphs snake colors!"),
            ("⚡ Speed Control", "Press 1-5 or +/- anytime to adjust snake velocity"),
            ("🛡️ Phase Shield", "Wrap through arena boundaries & gain tail immunity"),
            ("⏱️ Matrix Slow", "Bullet-time precision mode for crowded arenas"),
            ("✂️ Tail Trimmer", "Instantly trims tail length by 50%"),
            ("🌟 Super Star", "Immediate score explosion & combo surge"),
            ("🧲 Cyber Magnet", "Pulls nearby circular pies directly to you"),
        ]

        start_y = cy + 32
        for icon_name, desc in features:
            self.overlay_pen.goto(0, start_y)
            self.overlay_pen.color("#ffffff")
            self.overlay_pen.write(f"{icon_name}: {desc}", align="center", font=("Arial", 9, "normal"))
            start_y -= 19

        self.overlay_pen.goto(0, cy - 110)
        self.overlay_pen.color("#ffd700")
        self.overlay_pen.write("PRESS SPACE TO INITIALIZE SYSTEM", align="center", font=("Courier", 14, "bold"))

        self.overlay_pen.goto(0, cy - 134)
        self.overlay_pen.color(COLOR_MUTED)
        self.overlay_pen.write("Controls: Arrow Keys / WASD  |  Speed: 1-5, + / -  |  P: Pause  |  R: Reset", align="center", font=("Arial", 9, "normal"))

    def show_pause_screen(self):
        """Displays the pause banner."""
        self.overlay_pen.clear()
        cy = self.arena_offset_y

        self.overlay_pen.goto(0, cy + 20)
        self.overlay_pen.color("#ffd700")
        self.overlay_pen.write("⏸ SYSTEM PAUSED", align="center", font=("Helvetica", 24, "bold"))

        self.overlay_pen.goto(0, cy - 18)
        self.overlay_pen.color(COLOR_TEXT)
        self.overlay_pen.write("Press SPACE or P to Resume", align="center", font=("Courier", 13, "bold"))

    def show_game_over_screen(self):
        """Displays the persistent Game Over summary card with comprehensive gameplay statistics."""
        self.overlay_pen.clear()
        cy = self.arena_offset_y

        # Backdrop card for high contrast
        self.overlay_pen.goto(-280, cy - 110)
        self.overlay_pen.color("#0d111d")
        self.overlay_pen.begin_fill()
        for _ in range(2):
            self.overlay_pen.forward(560)
            self.overlay_pen.left(90)
            self.overlay_pen.forward(220)
            self.overlay_pen.left(90)
        self.overlay_pen.end_fill()

        # Border for card
        self.overlay_pen.pensize(2)
        self.overlay_pen.color(COLOR_FOOD_CORE)
        self.overlay_pen.pendown()
        for _ in range(2):
            self.overlay_pen.forward(560)
            self.overlay_pen.left(90)
            self.overlay_pen.forward(220)
            self.overlay_pen.left(90)
        self.overlay_pen.penup()

        # Game Over Banner
        self.overlay_pen.goto(0, cy + 72)
        self.overlay_pen.color(COLOR_FOOD_CORE)
        self.overlay_pen.write("SYSTEM OVERRIDE: GAME OVER", align="center", font=("Helvetica", 20, "bold"))

        # Score stats
        self.overlay_pen.goto(0, cy + 34)
        self.overlay_pen.color(COLOR_TEXT)
        self.overlay_pen.write(f"Final Score: {self.score}   |   High Score: {self.high_score}", align="center", font=("Arial", 13, "bold"))

        self.overlay_pen.goto(0, cy + 6)
        self.overlay_pen.color("#05d9e8")
        self.overlay_pen.write(f"Level: {self.level}   |   Pies Eaten: {self.foods_eaten}   |   Max Combo: x{self.max_combo}   |   Length: {len(self.segments) + 1}", align="center", font=("Arial", 10, "normal"))

        if self.score > 0 and self.score >= self.high_score:
            self.overlay_pen.goto(0, cy - 20)
            self.overlay_pen.color("#ffd700")
            self.overlay_pen.write("★ NEW HIGH SCORE RECORD ESTABLISHED! ★", align="center", font=("Arial", 11, "bold"))

        # Restart Call-to-action
        self.overlay_pen.goto(0, cy - 60)
        self.overlay_pen.color("#00ff87")
        self.overlay_pen.write("PRESS SPACE TO PLAY AGAIN", align="center", font=("Courier", 14, "bold"))

        self.overlay_pen.goto(0, cy - 88)
        self.overlay_pen.color(COLOR_MUTED)
        self.overlay_pen.write("Press R to Reset State", align="center", font=("Arial", 10, "normal"))

    def _setup_gradient_segments(self):
        """Recalculates dynamic color gradients across all body segments using current snake theme."""
        n = len(self.segments)
        if n == 0:
            return

        snake_theme = self._get_current_snake_theme()
        r1, g1, b1 = snake_theme["body_start"]
        r2, g2, b2 = snake_theme["body_end"]

        for idx, seg in enumerate(self.segments):
            factor = idx / max(n, 1)
            r = int(r1 + (r2 - r1) * factor)
            g = int(g1 + (b2 - g1) * factor)
            b = int(b1 + (b2 - b1) * factor)
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            seg.color(hex_color)

    def _update_eyes(self):
        """Repositions the snake's eyes based on travel direction."""
        hx = self.head.xcor()
        hy = self.head.ycor()
        d = self.head.direction

        if d == "up":
            self.eye_left.goto(hx - 5, hy + 4)
            self.eye_right.goto(hx + 5, hy + 4)
        elif d == "down":
            self.eye_left.goto(hx - 5, hy - 4)
            self.eye_right.goto(hx + 5, hy - 4)
        elif d == "left":
            self.eye_left.goto(hx - 4, hy + 5)
            self.eye_right.goto(hx - 4, hy - 5)
        elif d == "right":
            self.eye_left.goto(hx + 4, hy + 5)
            self.eye_right.goto(hx + 4, hy - 5)
        else:  # stopped
            self.eye_left.goto(hx - 4, hy + 4)
            self.eye_right.goto(hx + 4, hy + 4)

    def set_speed_level(self, lvl):
        """Sets manual snake speed preset (1-5)."""
        lvl = max(1, min(5, lvl))
        self.speed_level = lvl
        self.delay = SPEED_PRESETS[self.speed_level]["delay"]
        spd_name = SPEED_PRESETS[self.speed_level]["name"]
        self.popups.append(PopupText(self.head.xcor(), self.head.ycor() + 15, f"SPEED: {lvl} ({spd_name}) ⚡", "#00f2fe", font_size=11))
        self.update_hud()

    def speed_up(self):
        self.set_speed_level(self.speed_level + 1)

    def speed_down(self):
        self.set_speed_level(self.speed_level - 1)

    def _bind_keys(self):
        """Keyboard event bindings for movement, speed control, and state management."""
        self.screen.listen()

        # Directional controls
        self.screen.onkeypress(self.go_up, "Up")
        self.screen.onkeypress(self.go_down, "Down")
        self.screen.onkeypress(self.go_left, "Left")
        self.screen.onkeypress(self.go_right, "Right")

        self.screen.onkeypress(self.go_up, "w")
        self.screen.onkeypress(self.go_up, "W")
        self.screen.onkeypress(self.go_down, "s")
        self.screen.onkeypress(self.go_down, "S")
        self.screen.onkeypress(self.go_left, "a")
        self.screen.onkeypress(self.go_left, "A")
        self.screen.onkeypress(self.go_right, "d")
        self.screen.onkeypress(self.go_right, "D")

        # Speed Control bindings (1-5, +, -)
        self.screen.onkeypress(lambda: self.set_speed_level(1), "1")
        self.screen.onkeypress(lambda: self.set_speed_level(2), "2")
        self.screen.onkeypress(lambda: self.set_speed_level(3), "3")
        self.screen.onkeypress(lambda: self.set_speed_level(4), "4")
        self.screen.onkeypress(lambda: self.set_speed_level(5), "5")

        self.screen.onkeypress(self.speed_up, "plus")
        self.screen.onkeypress(self.speed_up, "equal")
        self.screen.onkeypress(self.speed_up, "]")
        self.screen.onkeypress(self.speed_down, "minus")
        self.screen.onkeypress(self.speed_down, "underscore")
        self.screen.onkeypress(self.speed_down, "[")

        # Game state controls
        self.screen.onkeypress(self.toggle_pause, "p")
        self.screen.onkeypress(self.toggle_pause, "P")
        self.screen.onkeypress(self.space_action, "space")
        self.screen.onkeypress(self.reset_game, "r")
        self.screen.onkeypress(self.reset_game, "R")

    def go_up(self):
        if self.state == "START":
            self.start_game()
        if self.head.direction != "down" and self.state == "PLAYING":
            self.head.direction = "up"

    def go_down(self):
        if self.state == "START":
            self.start_game()
        if self.head.direction != "up" and self.state == "PLAYING":
            self.head.direction = "down"

    def go_left(self):
        if self.state == "START":
            self.start_game()
        if self.head.direction != "right" and self.state == "PLAYING":
            self.head.direction = "left"

    def go_right(self):
        if self.state == "START":
            self.start_game()
        if self.head.direction != "left" and self.state == "PLAYING":
            self.head.direction = "right"

    def space_action(self):
        if self.state == "START" or self.state == "GAMEOVER":
            self.reset_game()
            self.start_game()
        elif self.state == "PAUSED":
            self.toggle_pause()
        elif self.state == "PLAYING":
            self.toggle_pause()

    def toggle_pause(self):
        if self.state == "PLAYING":
            self.state = "PAUSED"
            self.show_pause_screen()
        elif self.state == "PAUSED":
            self.state = "PLAYING"
            self.overlay_pen.clear()

    def start_game(self):
        self.state = "PLAYING"
        self.overlay_pen.clear()
        if self.head.direction == "stop":
            self.head.direction = "right"

    def trigger_shake(self, magnitude=4, frames=4):
        """Triggers a short camera shake for visceral tactile feedback."""
        self.shake_magnitude = magnitude
        self.shake_frames = frames

    def relocate_food(self):
        """Places the circular pie food at an empty grid position."""
        max_cx = (self.arena_limit_x - GRID_SIZE) // GRID_SIZE
        max_cy = (self.arena_limit_y - GRID_SIZE) // GRID_SIZE
        while True:
            gx = random.randint(-max_cx, max_cx) * GRID_SIZE
            gy = (random.randint(-max_cy, max_cy) * GRID_SIZE) + self.arena_offset_y

            head_hit = (gx, gy) == (self.head.xcor(), self.head.ycor())
            body_hit = any(seg.distance(gx, gy) < 15 for seg in self.segments)
            powerup_hit = (
                self.spawned_powerup is not None
                and self.powerup_core.distance(gx, gy) < 20
            )

            if not head_hit and not body_hit and not powerup_hit:
                self.food.goto(gx, gy)
                self.food_crust.goto(gx, gy)
                self.food_glow.goto(gx, gy)
                break

    def spawn_random_powerup(self):
        """Spawns a temporary cyber powerup item on the grid."""
        p_info = random.choice(POWERUP_TYPES)
        max_cx = (self.arena_limit_x - GRID_SIZE) // GRID_SIZE
        max_cy = (self.arena_limit_y - GRID_SIZE) // GRID_SIZE
        while True:
            gx = random.randint(-max_cx, max_cx) * GRID_SIZE
            gy = (random.randint(-max_cy, max_cy) * GRID_SIZE) + self.arena_offset_y

            if self.food.distance(gx, gy) > 40 and self.head.distance(gx, gy) > 40:
                self.spawned_powerup = p_info
                self.powerup_despawn_timer = 110  # Visible duration
                self.powerup_core.color(p_info["color"])
                self.powerup_glow.color(p_info["color"])
                self.powerup_core.goto(gx, gy)
                self.powerup_glow.goto(gx, gy)
                self.powerup_core.showturtle()
                self.powerup_glow.showturtle()
                break

    def hide_spawned_powerup(self):
        """Despawns the arena powerup pickup."""
        self.spawned_powerup = None
        self.powerup_core.hideturtle()
        self.powerup_glow.hideturtle()
        self.powerup_core.goto(2000, 2000)
        self.powerup_glow.goto(2000, 2000)

    def activate_powerup(self, p_info):
        """Applies a collected cyber powerup effect."""
        ptype = p_info["type"]
        self.trigger_shake(magnitude=5, frames=5)

        if ptype == "star":
            # Instant +60 points and +2 combo
            pts = 60 * max(1, self.combo)
            self.score += pts
            self.popups.append(PopupText(self.head.xcor(), self.head.ycor() + 15, f"+{pts} ★ SUPER!", "#ffd700", font_size=13))
            for _ in range(16):
                self.particles.append(Particle(self.head.xcor(), self.head.ycor(), "#ffd700", speed_range=(4, 9), size=0.4))
        elif ptype == "shrink":
            # Cuts snake length by up to 50%
            old_len = len(self.segments)
            keep_len = max(2, old_len // 2)
            removed = self.segments[keep_len:]
            self.segments = self.segments[:keep_len]
            for seg in removed:
                for _ in range(3):
                    self.particles.append(Particle(seg.xcor(), seg.ycor(), "#ff6b35", speed_range=(2, 6)))
                seg.hideturtle()
                seg.goto(2000, 2000)
            self._setup_gradient_segments()
            self.popups.append(PopupText(self.head.xcor(), self.head.ycor() + 15, "TAIL TRIMMED! ✂️", "#ff6b35", font_size=12))
        else:
            # Timed power-ups: shield, slow, magnet
            self.active_powerup = p_info
            self.powerup_timer = p_info["duration"]
            self.popups.append(PopupText(self.head.xcor(), self.head.ycor() + 15, p_info["name"], p_info["color"], font_size=12))
            for _ in range(12):
                self.particles.append(Particle(self.head.xcor(), self.head.ycor(), p_info["color"], speed_range=(3, 7)))

            if ptype == "shield":
                self.head.color(COLOR_HEAD_SHIELD)

        if self.score > self.high_score:
            self.high_score = self.score
        self.update_hud()

    def check_level_up(self):
        """Checks if enough food was eaten to level up and advance the cyberpunk theme."""
        new_level = (self.foods_eaten // 5) + 1
        if new_level != self.level:
            self.level = new_level
            theme = self._get_current_level_theme()
            self.draw_static_arena()
            self._setup_gradient_segments()
            self.popups.append(PopupText(0, self.arena_offset_y + 30, f"LEVEL UP: {theme['name']}!", theme["border"], font_size=15, life=22))
            self.trigger_shake(magnitude=6, frames=6)

    def trigger_eat_effect(self, x, y, is_combo=False):
        """Creates particle bursts, morphs snake color theme, and adds score popups."""
        # 1. Morph Snake Color Theme
        self.color_theme_index = (self.color_theme_index + 1) % len(SNAKE_COLOR_THEMES)
        new_snake_theme = self._get_current_snake_theme()

        # Update head color (unless shield is active)
        if not (self.active_powerup and self.active_powerup["type"] == "shield"):
            self.head.color(new_snake_theme["head"])

        # Recalculate gradient across all segments
        self._setup_gradient_segments()

        # 2. Score Calculation with combo
        base_points = 10
        multiplier = max(1, self.combo)
        earned = base_points * multiplier
        self.score += earned

        if self.score > self.high_score:
            self.high_score = self.score

        # Score & Color popup
        if self.combo > 1:
            popup_str = f"+{earned} (x{self.combo} COMBO!) 🎨"
            combo_col = "#ffd700" if self.combo >= 3 else new_snake_theme["sparkle"]
            self.popups.append(PopupText(x, y + 10, popup_str, combo_col, font_size=11 + min(self.combo, 3)))
        else:
            self.popups.append(PopupText(x, y + 10, f"+{earned} • {new_snake_theme['name']}", new_snake_theme["sparkle"]))

        # Particle burst (mix of food color and new snake color)
        part_count = 8 + min(self.combo * 2, 10)
        for _ in range(part_count // 2):
            self.particles.append(Particle(x, y, COLOR_FOOD_CORE))
            self.particles.append(Particle(x, y, new_snake_theme["sparkle"]))

    def trigger_game_over(self):
        """Ends the game with explosion particle effects and presents the persistent Game Over screen."""
        self.state = "GAMEOVER"
        self.hide_spawned_powerup()
        self.active_powerup = None

        snake_theme = self._get_current_snake_theme()
        self.head.color(snake_theme["head"])

        # Death explosion particles from head and segments
        hx, hy = self.head.xcor(), self.head.ycor()
        for _ in range(25):
            self.particles.append(Particle(hx, hy, COLOR_FOOD_CORE, speed_range=(4, 11), life=20, size=0.45))
            self.particles.append(Particle(hx, hy, "#00f2fe", speed_range=(3, 9), life=18, size=0.35))

        for seg in self.segments[:10]:
            for _ in range(3):
                self.particles.append(Particle(seg.xcor(), seg.ycor(), snake_theme["sparkle"], speed_range=(2, 6), life=15))

        self.trigger_shake(magnitude=7, frames=5)
        self.show_game_over_screen()

    def reset_game(self):
        """Resets the entire game state for a fresh run."""
        self.overlay_pen.clear()

        # Clear body segments
        for seg in self.segments:
            seg.goto(2000, 2000)
            seg.hideturtle()
        self.segments.clear()

        # Clear particles & popups
        for p in self.particles:
            p.t.hideturtle()
            p.t.goto(2000, 2000)
        self.particles.clear()
        for pop in self.popups:
            pop.t.clear()
        self.popups.clear()

        # Reset head, color & state
        self.color_theme_index = 0
        snake_theme = self._get_current_snake_theme()
        self.head.goto(0, self.arena_offset_y)
        self.head.direction = "stop"
        self.head.color(snake_theme["head"])
        self._update_eyes()

        self.score = 0
        self.level = 1
        self.foods_eaten = 0
        self.combo = 0
        self.combo_timer = 0
        self.max_combo = 0
        self.speed_level = DEFAULT_SPEED_LEVEL
        self.delay = SPEED_PRESETS[self.speed_level]["delay"]
        self.active_powerup = None
        self.powerup_timer = 0

        self.hide_spawned_powerup()
        self.relocate_food()
        self.draw_static_arena()
        self.update_hud()

    def run(self):
        """Main game loop."""
        pulse_frame = 0
        try:
            while True:
                # 0. Handle Screen Shake if active (during active playing)
                if self.shake_frames > 0:
                    self.shake_frames -= 1
                    sx = random.randint(-self.shake_magnitude, self.shake_magnitude)
                    sy = random.randint(-self.shake_magnitude, self.shake_magnitude)
                    self.draw_static_arena(shake_x=sx, shake_y=sy)
                    if self.shake_frames == 0:
                        self.draw_static_arena()
                    # If gameover occurred during shake, ensure overlay is preserved
                    if self.state == "GAMEOVER":
                        self.show_game_over_screen()

                self.screen.update()

                # Update visual particles & text popups
                self.particles = [p for p in self.particles if p.update()]
                self.popups = [pop for pop in self.popups if pop.update()]

                if self.state == "PLAYING":
                    pulse_frame += 1

                    # Pulsing glow animation on circular pie food
                    glow_scale = 1.25 + 0.22 * math.sin(pulse_frame * 0.3)
                    self.food_glow.shapesize(glow_scale, glow_scale)

                    # Update combo timer
                    if self.combo_timer > 0:
                        self.combo_timer -= 1
                        if self.combo_timer == 0:
                            self.combo = 0
                            self.update_hud()

                    # Handle active power-up duration
                    if self.active_powerup and self.powerup_timer > 0:
                        self.powerup_timer -= 1

                        # Magnet effect: Pull circular pie 1 step closer every 4 ticks
                        if self.active_powerup["type"] == "magnet" and pulse_frame % 4 == 0:
                            fx, fy = self.food.xcor(), self.food.ycor()
                            hx, hy = self.head.xcor(), self.head.ycor()
                            if abs(fx - hx) >= GRID_SIZE and random.random() < 0.7:
                                fx += GRID_SIZE if fx < hx else -GRID_SIZE
                            if abs(fy - hy) >= GRID_SIZE and random.random() < 0.7:
                                fy += GRID_SIZE if fy < hy else -GRID_SIZE
                            self.food.goto(fx, fy)
                            self.food_crust.goto(fx, fy)
                            self.food_glow.goto(fx, fy)

                        if self.powerup_timer <= 0:
                            self.active_powerup = None
                            snake_theme = self._get_current_snake_theme()
                            self.head.color(snake_theme["head"])
                        self.update_hud()

                    # Handle arena powerup animation & despawn timer
                    if self.spawned_powerup:
                        self.powerup_despawn_timer -= 1
                        p_scale = 1.2 + 0.3 * math.sin(pulse_frame * 0.4)
                        self.powerup_glow.shapesize(p_scale, p_scale)
                        if self.powerup_despawn_timer <= 0:
                            self.hide_spawned_powerup()

                    # 1. Check Wall Collisions (Wrap around if Shield is active, else Game Over)
                    bound_x = self.arena_limit_x - 8
                    bound_y = self.arena_limit_y - 8
                    cy = self.arena_offset_y
                    hx, hy = self.head.xcor(), self.head.ycor()

                    hit_wall = (
                        abs(hx) > bound_x
                        or hy > (cy + bound_y)
                        or hy < (cy - bound_y)
                    )

                    is_shielded = self.active_powerup and self.active_powerup["type"] == "shield"

                    if hit_wall:
                        if is_shielded:
                            # Wrap around rectangular arena walls
                            max_cx = (self.arena_limit_x - GRID_SIZE) // GRID_SIZE
                            max_cy = (self.arena_limit_y - GRID_SIZE) // GRID_SIZE
                            if hx > bound_x:
                                self.head.setx(-max_cx * GRID_SIZE)
                            elif hx < -bound_x:
                                self.head.setx(max_cx * GRID_SIZE)
                            if hy > (cy + bound_y):
                                self.head.sety(cy - max_cy * GRID_SIZE)
                            elif hy < (cy - bound_y):
                                self.head.sety(cy + max_cy * GRID_SIZE)
                        else:
                            self.trigger_game_over()
                            continue

                    # 2. Check Circular Pie Food Collision
                    if self.head.distance(self.food) < GRID_SIZE:
                        fx, fy = self.food.xcor(), self.food.ycor()

                        # Combo update
                        if self.combo_timer > 0:
                            self.combo += 1
                        else:
                            self.combo = 1
                        self.combo_timer = 32  # Combo window
                        if self.combo > self.max_combo:
                            self.max_combo = self.combo

                        self.trigger_eat_effect(fx, fy, is_combo=(self.combo > 1))
                        self.relocate_food()

                        # Add new segment
                        new_seg = turtle.Turtle()
                        new_seg.speed(0)
                        new_seg.shape("circle")
                        new_seg.shapesize(0.9, 0.9)
                        new_seg.penup()
                        self.segments.append(new_seg)
                        self._setup_gradient_segments()

                        # Progression
                        self.foods_eaten += 1
                        self.check_level_up()
                        self.update_hud()

                        # Spawn special powerup every 4 foods
                        if self.foods_eaten % 4 == 0 and not self.spawned_powerup:
                            self.spawn_random_powerup()

                    # 3. Check Arena Powerup Pickup Collision
                    if self.spawned_powerup and self.head.distance(self.powerup_core) < GRID_SIZE + 4:
                        collected = self.spawned_powerup
                        self.hide_spawned_powerup()
                        self.activate_powerup(collected)

                    # 4. Move Body Segments
                    for i in range(len(self.segments) - 1, 0, -1):
                        x = self.segments[i - 1].xcor()
                        y = self.segments[i - 1].ycor()
                        self.segments[i].goto(x, y)

                    if self.segments:
                        self.segments[0].goto(self.head.xcor(), self.head.ycor())

                    # 5. Move Head
                    if self.head.direction == "up":
                        self.head.sety(self.head.ycor() + GRID_SIZE)
                    elif self.head.direction == "down":
                        self.head.sety(self.head.ycor() - GRID_SIZE)
                    elif self.head.direction == "left":
                        self.head.setx(self.head.xcor() - GRID_SIZE)
                    elif self.head.direction == "right":
                        self.head.setx(self.head.xcor() + GRID_SIZE)

                    self._update_eyes()

                    # 6. Check Self Tail Collision (Ignored if shielded)
                    if not is_shielded:
                        for seg in self.segments:
                            if seg.distance(self.head) < 12:
                                self.trigger_game_over()
                                break

                # Slow-mo effect adjusts loop delay
                current_delay = self.delay
                if self.active_powerup and self.active_powerup["type"] == "slow":
                    current_delay = self.delay * 1.65

                time.sleep(current_delay if self.state == "PLAYING" else 0.04)

        except turtle.Terminator:
            pass


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
