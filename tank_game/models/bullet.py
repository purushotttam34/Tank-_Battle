from __future__ import annotations

import math

from tank_game import constants as const


class Bullet:
    def __init__(self, x: float, y: float, angle: float, owner: int) -> None:
        self.x = x
        self.y = y
        self.angle = angle
        self.speed: float = const.BULLET_SPEED
        self.radius: int = const.BULLET_RADIUS
        self.owner = owner

    def update(self) -> None:
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

    def draw(self, screen) -> None:
        pygame.draw.circle(
            screen, (255, 215, 0), (int(self.x), int(self.y)), self.radius
        )

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )


import pygame
