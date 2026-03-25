from __future__ import annotations

import math

import pygame

from tank_game import constants as const
from tank_game.models import Tank


def has_line_of_sight(
    attacker: Tank, target: Tank, obstacles: list[pygame.Rect]
) -> bool:
    dx = target.x - attacker.x
    dy = target.y - attacker.y
    dist = math.hypot(dx, dy)
    if dist < 30:
        return True

    steps = max(8, int(dist / 9))
    for i in range(1, steps):
        px = attacker.x + dx * i / steps
        py = attacker.y + dy * i / steps
        check_rect = pygame.Rect(px - 5, py - 5, 10, 10)
        if any(check_rect.colliderect(obs) for obs in obstacles):
            return False
    return True


def check_bullet_collision(
    bullet,
    obstacles: list[pygame.Rect],
    tank1: Tank | None,
    tank2: Tank | None,
) -> tuple[bool, Tank | None]:
    bullet_rect = bullet.get_rect()

    if not (
        0 < bullet.x < const.WIDTH and 0 < bullet.y < const.HEIGHT
    ) or any(bullet_rect.colliderect(o) for o in obstacles):
        return True, None

    for tank in (tank1, tank2):
        if tank and tank.player_num != bullet.owner:
            tank_rect = pygame.Rect(
                tank.x - const.TANK_WIDTH // 2,
                tank.y - const.TANK_HEIGHT // 2,
                const.TANK_WIDTH,
                const.TANK_HEIGHT,
            )
            if bullet_rect.colliderect(tank_rect):
                tank.health -= const.BULLET_DAMAGE
                return True, tank

    return False, None
