from __future__ import annotations

import random
from enum import Enum, auto

import pygame

from tank_game import constants as const
from tank_game.models import Tank, Bullet
from tank_game.utils.maps import find_safe_position


class GameState(Enum):
    MAIN = auto()
    SUBMENU = auto()
    GAME = auto()
    PAUSE = auto()
    WINNER = auto()


class GameManager:
    def __init__(self) -> None:
        self.state: GameState = GameState.MAIN
        self.tank1: Tank | None = None
        self.tank2: Tank | None = None
        self.bullets: list[Bullet] = []
        self.obstacles: list[pygame.Rect] = []
        self.game_start_time: int = 0
        self.two_player_mode: bool = False
        self.last_with_bot: bool = True
        self.paused: bool = False
        self.winner: str | None = None

    def start_new_game(self, with_bot: bool) -> None:
        self.two_player_mode = not with_bot
        self.last_with_bot = with_bot
        self.paused = False
        self.winner = None
        self.bullets = []
        self.game_start_time = pygame.time.get_ticks()
        self.obstacles = random.choice(const.map_list).copy()

        x1, y1 = find_safe_position("left", self.obstacles)
        x2, y2 = find_safe_position("right", self.obstacles)

        self.tank1 = Tank(x1, y1, 0, const.RED, 1)
        self.tank2 = Tank(x2, y2, 180, const.BLUE, 2)

        if not self.two_player_mode:
            self.tank2.speed = const.BOT_SPEED
            self.tank2.rot_speed = const.BOT_ROT_SPEED

        self.state = GameState.GAME

    def update_tanks_ammo(self) -> None:
        if self.tank1 and self.tank2:
            self.tank1.update_ammo(self.game_start_time)
            self.tank2.update_ammo(self.game_start_time)

    def get_winner_text(self) -> str:
        if not self.winner:
            return ""
        if self.two_player_mode:
            return f"Player {self.winner} Wins!"
        return "YOU WIN!" if self.winner == 1 else "BOT Wins!"

    def reset_to_main(self) -> None:
        self.state = GameState.MAIN
        self.paused = False
        self.winner = None
