from __future__ import annotations

import random

import pygame

from tank_game import constants as const


def find_safe_position(
    side: str, obstacles: list[pygame.Rect]
) -> tuple[int, int]:
    if side == "left":
        x_range = range(100, 240)
    else:
        x_range = range(const.WIDTH - 240, const.WIDTH - 100)

    for _ in range(120):
        x = random.choice(list(x_range))
        y = random.randint(160, const.HEIGHT - 160)
        test_rect = pygame.Rect(
            x - const.TANK_WIDTH // 2,
            y - const.TANK_HEIGHT // 2,
            const.TANK_WIDTH,
            const.TANK_HEIGHT,
        )
        if not any(test_rect.colliderect(obs) for obs in obstacles):
            return x, y

    return (
        (160, const.HEIGHT // 2)
        if side == "left"
        else (const.WIDTH - 160, const.HEIGHT // 2)
    )
