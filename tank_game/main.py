from __future__ import annotations

import sys

import pygame

from tank_game import constants as const
from tank_game.game_state import GameManager, GameState
from tank_game.ai import ai_control
from tank_game.audio import get_sound_manager
from tank_game import renderer
from tank_game import ui


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
    pygame.display.set_caption("Tank Battle - Refactored")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("arial", 36)
    small_font = pygame.font.SysFont("arial", 24)
    big_font = pygame.font.SysFont("arial", 62, bold=True)

    sound_manager = get_sound_manager()
    sound_manager.play_music()

    game = GameManager()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                if screen.get_flags() & pygame.FULLSCREEN:
                    screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
                else:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                if game.state == GameState.MAIN:
                    if not ui.handle_menu_click(game, mx, my):
                        running = False

                elif game.state == GameState.SUBMENU:
                    ui.handle_menu_click(game, mx, my)

                elif game.state == GameState.GAME:
                    ui.handle_game_click(game, mx, my)

                elif game.state == GameState.WINNER:
                    ui.handle_winner_click(game, mx, my)

        keys = pygame.key.get_pressed()

        if game.state == GameState.GAME and not game.paused:
            _handle_player_input(keys, game, sound_manager)
            _update_game(game, sound_manager)

        if game.state in (GameState.GAME, GameState.PAUSE, GameState.WINNER):
            renderer.draw_game(screen, game, font, small_font)
        else:
            renderer.draw_background(screen)

        if game.state == GameState.MAIN:
            ui.draw_main_menu(screen, font, big_font)

        elif game.state == GameState.SUBMENU:
            ui.draw_submenu(screen, font, small_font)

        elif game.paused:
            ui.draw_pause_menu(screen, font, big_font)

        if game.state == GameState.WINNER:
            ui.draw_winner_screen(screen, game.get_winner_text(), font, big_font)

        pygame.display.flip()
        clock.tick(const.FPS)

    pygame.quit()
    sys.exit()


def _handle_player_input(keys, game: GameManager, sound_manager) -> None:
    if not game.tank1 or not game.tank2:
        return

    if keys[pygame.K_w]:
        game.tank1.angle = 270
        game.tank1.move(True, game.obstacles, game.tank2)
    if keys[pygame.K_s]:
        game.tank1.angle = 90
        game.tank1.move(True, game.obstacles, game.tank2)
    if keys[pygame.K_a]:
        game.tank1.angle = 180
        game.tank1.move(True, game.obstacles, game.tank2)
    if keys[pygame.K_d]:
        game.tank1.angle = 0
        game.tank1.move(True, game.obstacles, game.tank2)
    if keys[pygame.K_SPACE]:
        game.tank1.shoot(game.bullets, sound_manager)

    if game.two_player_mode:
        if keys[pygame.K_UP]:
            game.tank2.angle = 270
            game.tank2.move(True, game.obstacles, game.tank1)
        if keys[pygame.K_DOWN]:
            game.tank2.angle = 90
            game.tank2.move(True, game.obstacles, game.tank1)
        if keys[pygame.K_LEFT]:
            game.tank2.angle = 180
            game.tank2.move(True, game.obstacles, game.tank1)
        if keys[pygame.K_RIGHT]:
            game.tank2.angle = 0
            game.tank2.move(True, game.obstacles, game.tank1)
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            game.tank2.shoot(game.bullets, sound_manager)
    else:
        ai_control(game.tank2, game.tank1, game.obstacles, game.bullets)


def _update_game(game: GameManager, sound_manager) -> None:
    game.update_tanks_ammo()

    for b in game.bullets[:]:
        b.update()
        from tank_game.utils.physics import check_bullet_collision

        hit, tank = check_bullet_collision(
            b, game.obstacles, game.tank1, game.tank2
        )
        if hit:
            game.bullets.remove(b)
            if tank and tank.health <= 0:
                game.set_winner(b.owner)


if __name__ == "__main__":
    main()
