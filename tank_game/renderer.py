from __future__ import annotations

import pygame

from tank_game import constants as const
from tank_game.models import Tank, Bullet
from tank_game.game_state import GameManager


def draw_background(screen: pygame.Surface) -> None:
    screen.fill(const.SKY)
    pygame.draw.rect(
        screen, const.GROUND, (0, const.HEIGHT - 85, const.WIDTH, 85)
    )


def draw_obstacles(screen: pygame.Surface, obstacles: list[pygame.Rect]) -> None:
    for obs in obstacles:
        pygame.draw.rect(screen, const.BOX_COLOR, obs)
        pygame.draw.rect(screen, (80, 40, 10), obs, 7)


def draw_tanks(screen: pygame.Surface, tank1: Tank, tank2: Tank) -> None:
    tank1.draw(screen)
    tank2.draw(screen)


def draw_bullets(screen: pygame.Surface, bullets: list[Bullet]) -> None:
    for b in bullets:
        b.draw(screen)


def draw_hud(
    screen: pygame.Surface, tank1: Tank, tank2: Tank, font: pygame.font.Font
) -> None:
    pygame.draw.rect(
        screen,
        (30, 30, 30),
        (25, const.HEIGHT - 62, 260, 48),
        border_radius=8,
    )
    pygame.draw.rect(
        screen,
        const.WHITE,
        (25, const.HEIGHT - 62, 260, 48),
        4,
        border_radius=8,
    )
    screen.blit(
        font.render(f"P1 Bullets: {tank1.ammo}/7", True, const.WHITE),
        (42, const.HEIGHT - 53),
    )

    pygame.draw.rect(
        screen,
        (30, 30, 30),
        (const.WIDTH - 285, const.HEIGHT - 62, 260, 48),
        border_radius=8,
    )
    pygame.draw.rect(
        screen,
        const.WHITE,
        (const.WIDTH - 285, const.HEIGHT - 62, 260, 48),
        4,
        border_radius=8,
    )
    screen.blit(
        font.render(f"P2 Bullets: {tank2.ammo}/7", True, const.WHITE),
        (const.WIDTH - 268, const.HEIGHT - 53),
    )


def draw_pause_button(screen: pygame.Surface, font: pygame.font.Font) -> None:
    pause_rect = pygame.Rect(const.WIDTH - 65, 15, 50, 50)
    pygame.draw.rect(screen, (230, 230, 230), pause_rect, border_radius=10)
    screen.blit(font.render("||", True, const.BLACK), (const.WIDTH - 54, 19))


def draw_game(
    screen: pygame.Surface,
    game: GameManager,
    font: pygame.font.Font,
    small_font: pygame.font.Font,
) -> None:
    draw_background(screen)
    draw_obstacles(screen, game.obstacles)

    if game.tank1 and game.tank2:
        draw_tanks(screen, game.tank1, game.tank2)
        draw_bullets(screen, game.bullets)
        draw_hud(screen, game.tank1, game.tank2, small_font)
        draw_pause_button(screen, font)
