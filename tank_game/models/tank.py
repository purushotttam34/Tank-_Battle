from __future__ import annotations

import math
from pathlib import Path

import pygame

from tank_game import constants as const


class Tank:
    def __init__(
        self,
        x: float,
        y: float,
        angle: float,
        color: tuple[int, int, int],
        player_num: int,
    ) -> None:
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color
        self.player_num = player_num
        self.health: int = const.TANK_HEALTH
        self.ammo: int = const.TANK_MAX_AMMO
        self.max_ammo: int = const.TANK_MAX_AMMO
        self.speed: float = const.TANK_SPEED
        self.rot_speed: float = const.TANK_ROT_SPEED
        self.last_regen: int = pygame.time.get_ticks()
        self.last_shot: int = pygame.time.get_ticks()
        self.surf: pygame.Surface = self._load_sprite()

    def _load_sprite(self) -> pygame.Surface:
        sprite_path = (
            Path(__file__).parent.parent.parent
            / "sprites"
            / f"Player{self.player_num}.png"
        )
        if sprite_path.exists():
            surf = pygame.image.load(sprite_path).convert_alpha()
            return pygame.transform.scale(surf, (74, 48))
        return self._create_fallback_surface()

    def _create_fallback_surface(self) -> pygame.Surface:
        surf = pygame.Surface((74, 48), pygame.SRCALPHA)
        pygame.draw.rect(surf, (50, 50, 50), (4, 5, 66, 13))
        pygame.draw.rect(surf, (50, 50, 50), (4, 30, 66, 13))
        pygame.draw.rect(surf, self.color, (12, 12, 50, 26))
        pygame.draw.circle(surf, self.color, (46, 25), 15)
        pygame.draw.rect(surf, const.BLACK, (52, 20, 28, 9))
        return surf

    def draw(self, screen: pygame.Surface) -> None:
        rotated = pygame.transform.rotate(self.surf, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated, rect.topleft)
        self._draw_health_bar(screen)

    def _draw_health_bar(self, screen: pygame.Surface) -> None:
        bar_w = 66
        ratio = max(self.health, 0) / const.TANK_HEALTH
        pygame.draw.rect(
            screen, const.BLACK, (self.x - bar_w // 2, self.y - 48, bar_w, 9)
        )
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (self.x - bar_w // 2, self.y - 48, int(bar_w * ratio), 9),
        )

    def move(
        self,
        forward: bool,
        obstacles: list[pygame.Rect],
        other_tank: Tank | None = None,
    ) -> None:
        dx = math.cos(math.radians(self.angle)) * self.speed
        dy = math.sin(math.radians(self.angle)) * self.speed
        if not forward:
            dx = -dx
            dy = -dy

        new_x = self.x + dx
        new_y = self.y + dy

        tank_rect = pygame.Rect(
            new_x - const.TANK_WIDTH // 2,
            new_y - const.TANK_HEIGHT // 2,
            const.TANK_WIDTH,
            const.TANK_HEIGHT,
        )

        if (
            tank_rect.left < const.SCREEN_MARGIN
            or tank_rect.right > const.WIDTH - const.SCREEN_MARGIN
            or tank_rect.top < const.SCREEN_MARGIN
            or tank_rect.bottom > const.HEIGHT - const.SCREEN_MARGIN
        ):
            return

        for obs in obstacles:
            if tank_rect.colliderect(obs):
                return

        if other_tank:
            other_rect = pygame.Rect(
                other_tank.x - const.TANK_WIDTH // 2,
                other_tank.y - const.TANK_HEIGHT // 2,
                const.TANK_WIDTH,
                const.TANK_HEIGHT,
            )
            if tank_rect.colliderect(other_rect):
                return

        self.x = new_x
        self.y = new_y

    def rotate(self, direction: int) -> None:
        self.angle = (self.angle + direction * self.rot_speed) % 360

    def update_ammo(self, game_start_time: int) -> None:
        now = pygame.time.get_ticks()
        elapsed = now - game_start_time
        interval = (
            const.REGEN_INTERVAL_FAST
            if elapsed < const.REGEN_THRESHOLD
            else const.REGEN_INTERVAL_SLOW
        )
        if now - self.last_regen > interval and self.ammo < self.max_ammo:
            self.ammo += 1
            self.last_regen = now

    def shoot(self, bullets_list: list, sound_manager=None) -> None:
        now = pygame.time.get_ticks()
        owner_bullets = [b for b in bullets_list if b.owner == self.player_num]

        if (
            self.ammo > 0
            and now - self.last_shot > const.SHOT_COOLDOWN
            and len(owner_bullets) < const.BULLET_LIMIT
        ):
            from tank_game.models import Bullet

            bx = self.x + math.cos(math.radians(self.angle)) * const.BULLET_SPAWN_OFFSET
            by = self.y + math.sin(math.radians(self.angle)) * const.BULLET_SPAWN_OFFSET
            bullets_list.append(Bullet(bx, by, self.angle, self.player_num))
            self.ammo -= 1
            self.last_shot = now
            if sound_manager:
                sound_manager.play_shoot()
