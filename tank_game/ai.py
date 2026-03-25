from __future__ import annotations

import math
import random

import pygame

from tank_game import constants as const
from tank_game.models import Tank, Bullet
from tank_game.utils.physics import has_line_of_sight


def ai_control(
    bot: Tank,
    target: Tank,
    obstacles: list[pygame.Rect],
    bullets_list: list[Bullet],
) -> None:
    dx = target.x - bot.x
    dy = target.y - bot.y
    target_angle = math.degrees(math.atan2(dy, dx))
    dist = math.hypot(dx, dy)
    los = has_line_of_sight(bot, target, obstacles)

    dodge_angle = _dodge_bullets(bot, bullets_list)
    if dodge_angle is not None:
        _execute_dodge(bot, target, obstacles, dodge_angle)
        return

    angle_diff = (target_angle - bot.angle + 180) % 360 - 180
    if abs(angle_diff) > 4:
        bot.rotate(1 if angle_diff > 0 else -1)

    if los and abs(angle_diff) < 11 and dist < 530 and random.random() < 0.068:
        bot.shoot(bullets_list)

    if dist > 158:
        best_angle = _find_best_angle(bot, target, obstacles, target_angle)
        best_diff = (best_angle - bot.angle + 180) % 360 - 180
        if abs(best_diff) > 6:
            bot.rotate(1 if best_diff > 0 else -1)
        bot.move(True, obstacles, target)

    elif dist < 115:
        bot.move(False, obstacles, target)
        if random.random() < 0.38:
            bot.rotate(random.choice([34, -34]))

    if not los and random.random() < 0.055:
        bot.rotate(random.choice([47, -47]))
        bot.move(True, obstacles, target)


def _dodge_bullets(
    bot: Tank, bullets_list: list[Bullet]
) -> float | None:
    for b in bullets_list:
        if b.owner != bot.player_num:
            bdx = b.x - bot.x
            bdy = b.y - bot.y
            bdist = math.hypot(bdx, bdy)
            if 12 < bdist < 145:
                dx_from_bullet_to_bot = bot.x - b.x
                dy_from_bullet_to_bot = bot.y - b.y
                dir_from_bullet = math.degrees(
                    math.atan2(dy_from_bullet_to_bot, dx_from_bullet_to_bot)
                )
                heading_diff = (dir_from_bullet - b.angle + 180) % 360 - 180
                if abs(heading_diff) < 37:
                    return (b.angle + (90 if random.random() < 0.5 else -90)) % 360
    return None


def _execute_dodge(
    bot: Tank,
    target: Tank,
    obstacles: list[pygame.Rect],
    dodge_angle: float,
) -> None:
    diff = (dodge_angle - bot.angle + 180) % 360 - 180
    bot.rotate(1 if diff > 0 else -1)
    bot.move(True, obstacles, target)


def _find_best_angle(
    bot: Tank,
    target: Tank,
    obstacles: list[pygame.Rect],
    target_angle: float,
) -> float:
    best_angle = bot.angle
    best_score = -999999

    for offset in range(-84, 85, 12):
        test_angle = (target_angle + offset) % 360
        sim_x = bot.x
        sim_y = bot.y
        collided = False
        steps_taken = 0

        for step in range(14):
            sx = math.cos(math.radians(test_angle)) * bot.speed
            sy = math.sin(math.radians(test_angle)) * bot.speed
            sim_x += sx
            sim_y += sy
            steps_taken += 1

            sim_rect = pygame.Rect(
                sim_x - const.TANK_WIDTH // 2,
                sim_y - const.TANK_HEIGHT // 2,
                const.TANK_WIDTH,
                const.TANK_HEIGHT,
            )

            if (
                sim_rect.left < const.SCREEN_MARGIN
                or sim_rect.right > const.WIDTH - const.SCREEN_MARGIN
                or sim_rect.top < const.SCREEN_MARGIN
                or sim_rect.bottom > const.HEIGHT - const.SCREEN_MARGIN
            ):
                collided = True
                break

            for obs in obstacles:
                if sim_rect.colliderect(obs):
                    collided = True
                    break
            if collided:
                break

        if collided:
            continue

        final_dist = math.hypot(target.x - sim_x, target.y - sim_y)
        score = -final_dist * 1.2 + steps_taken * 6.5

        if score > best_score:
            best_score = score
            best_angle = test_angle

    return best_angle
