from pygame import Rect
from typing import Final

WIDTH: Final[int] = 1000
HEIGHT: Final[int] = 650

SKY: tuple[int, int, int] = (135, 206, 235)
GROUND: tuple[int, int, int] = (34, 139, 34)
BOX_COLOR: tuple[int, int, int] = (139, 69, 19)
RED: tuple[int, int, int] = (200, 0, 0)
BLUE: tuple[int, int, int] = (0, 0, 200)
BLACK: tuple[int, int, int] = (20, 20, 20)
WHITE: tuple[int, int, int] = (255, 255, 255)

TANK_SPEED: Final[float] = 3.8
TANK_ROT_SPEED: Final[float] = 3.8
BOT_SPEED: Final[float] = 2.5
BOT_ROT_SPEED: Final[float] = 2.9

TANK_HEALTH: Final[int] = 100
TANK_MAX_AMMO: Final[int] = 7
BULLET_DAMAGE: Final[int] = 34
BULLET_SPEED: Final[float] = 9
BULLET_RADIUS: Final[int] = 6

SHOT_COOLDOWN: Final[int] = 380
BULLET_LIMIT: Final[int] = 5

REGEN_INTERVAL_FAST: Final[int] = 1000
REGEN_INTERVAL_SLOW: Final[int] = 2000
REGEN_THRESHOLD: Final[int] = 5000

SCREEN_MARGIN: Final[int] = 15
TANK_WIDTH: Final[int] = 48
TANK_HEIGHT: Final[int] = 32
BULLET_SPAWN_OFFSET: Final[float] = 34.0

FPS: Final[int] = 60

map_list: list[list[Rect]] = [
    [
        Rect(250, 90, 40, 200),
        Rect(250, 360, 40, 200),
        Rect(420, 200, 200, 40),
        Rect(680, 90, 40, 240),
        Rect(100, 240, 130, 40),
    ],
    [
        Rect(300, 140, 380, 35),
        Rect(300, 470, 380, 35),
        Rect(200, 210, 35, 220),
        Rect(750, 210, 35, 220),
        Rect(420, 260, 160, 130),
    ],
    [
        Rect(150, 80, 65, 340),
        Rect(780, 80, 65, 340),
        Rect(270, 160, 480, 45),
        Rect(270, 445, 480, 45),
        Rect(370, 260, 45, 130),
        Rect(580, 260, 45, 130),
    ],
    [
        Rect(110, 100, 100, 100),
        Rect(220, 440, 100, 100),
        Rect(430, 150, 100, 100),
        Rect(640, 390, 100, 100),
        Rect(800, 210, 100, 100),
        Rect(310, 310, 200, 45),
    ],
    [
        Rect(150, 150, 700, 35),
        Rect(150, 465, 700, 35),
        Rect(310, 210, 35, 240),
        Rect(655, 210, 35, 240),
        Rect(90, 300, 130, 45),
        Rect(780, 300, 130, 45),
    ],
]
