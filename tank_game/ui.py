from __future__ import annotations

import pygame

from tank_game import constants as const


def draw_button(
    screen: pygame.Surface,
    text: str,
    rect: pygame.Rect,
    color: tuple[int, int, int],
    font: pygame.font.Font,
) -> None:
    pygame.draw.rect(screen, color, rect, border_radius=15)
    pygame.draw.rect(screen, const.BLACK, rect, 5, border_radius=15)
    txt = font.render(text, True, const.WHITE)
    screen.blit(txt, txt.get_rect(center=rect.center))


def draw_main_menu(
    screen: pygame.Surface, font: pygame.font.Font, big_font: pygame.font.Font
) -> None:
    title = big_font.render("TANK BATTLE", True, (220, 20, 20))
    screen.blit(title, (const.WIDTH // 2 - title.get_width() // 2, 90))
    draw_button(
        screen,
        "PLAY",
        pygame.Rect(300, 220, 400, 70),
        (50, 160, 50),
        font,
    )
    draw_button(
        screen,
        "EXIT",
        pygame.Rect(300, 320, 400, 70),
        (180, 40, 40),
        font,
    )


def draw_submenu(
    screen: pygame.Surface, font: pygame.font.Font, small_font: pygame.font.Font
) -> None:
    screen.blit(
        small_font.render("Choose Mode", True, const.WHITE),
        (const.WIDTH // 2 - 90, 120),
    )
    draw_button(
        screen,
        "Play with Bot",
        pygame.Rect(300, 200, 400, 70),
        (40, 100, 200),
        font,
    )
    draw_button(
        screen,
        "Play with Friend",
        pygame.Rect(300, 290, 400, 70),
        (40, 100, 200),
        font,
    )
    draw_button(
        screen,
        "Back",
        pygame.Rect(300, 400, 400, 60),
        (140, 140, 140),
        font,
    )


def draw_pause_menu(
    screen: pygame.Surface, font: pygame.font.Font, big_font: pygame.font.Font
) -> None:
    overlay = pygame.Surface((const.WIDTH, const.HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    screen.blit(font.render("PAUSED", True, const.WHITE), (const.WIDTH // 2 - 85, 170))
    draw_button(
        screen,
        "RESUME",
        pygame.Rect(const.WIDTH // 2 - 160, 260, 320, 75),
        (50, 160, 50),
        font,
    )
    draw_button(
        screen,
        "MAIN MENU",
        pygame.Rect(const.WIDTH // 2 - 160, 360, 320, 75),
        (180, 50, 50),
        font,
    )


def draw_winner_screen(
    screen: pygame.Surface,
    winner: str,
    font: pygame.font.Font,
    big_font: pygame.font.Font,
) -> None:
    overlay = pygame.Surface((const.WIDTH, const.HEIGHT))
    overlay.set_alpha(170)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    win_text = big_font.render(winner, True, (255, 215, 0))
    screen.blit(
        win_text,
        (const.WIDTH // 2 - win_text.get_width() // 2, const.HEIGHT // 2 - 110),
    )
    draw_button(
        screen,
        "RESTART",
        pygame.Rect(const.WIDTH // 2 - 190, const.HEIGHT // 2 + 70, 190, 70),
        (50, 160, 50),
        font,
    )
    draw_button(
        screen,
        "MAIN MENU",
        pygame.Rect(const.WIDTH // 2 + 30, const.HEIGHT // 2 + 70, 230, 70),
        (180, 50, 50),
        font,
    )


def handle_menu_click(
    game,
    mx: int,
    my: int,
) -> bool:
    if game.state.value == 1:
        if 300 <= mx <= 700 and 220 <= my <= 290:
            game.state = game.state.__class__.SUBMENU
            return True
        if 300 <= mx <= 700 and 320 <= my <= 390:
            return False

    elif game.state.value == 2:
        if 300 <= mx <= 700 and 200 <= my <= 270:
            game.start_new_game(True)
            return True
        if 300 <= mx <= 700 and 290 <= my <= 360:
            game.start_new_game(False)
            return True
        if 300 <= mx <= 700 and 400 <= my <= 460:
            game.state = game.state.__class__.MAIN
            return True

    return True


def handle_game_click(game, mx: int, my: int) -> bool:
    pause_rect = pygame.Rect(const.WIDTH - 65, 15, 50, 50)
    if pause_rect.collidepoint(mx, my) and not game.paused:
        game.paused = True
        return True
    elif game.paused:
        resume_rect = pygame.Rect(const.WIDTH // 2 - 160, 260, 320, 75)
        menu_rect = pygame.Rect(const.WIDTH // 2 - 160, 360, 320, 75)
        if resume_rect.collidepoint(mx, my):
            game.paused = False
        elif menu_rect.collidepoint(mx, my):
            game.reset_to_main()
        return True
    return True


def handle_winner_click(game, mx: int, my: int) -> bool:
    restart_rect = pygame.Rect(const.WIDTH // 2 - 190, const.HEIGHT // 2 + 70, 190, 70)
    menu_rect = pygame.Rect(const.WIDTH // 2 + 30, const.HEIGHT // 2 + 70, 230, 70)
    if restart_rect.collidepoint(mx, my):
        game.start_new_game(game.last_with_bot)
    elif menu_rect.collidepoint(mx, my):
        game.reset_to_main()
    return True
