import pygame
import math
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Battle - Ultra Smart AI + Fixed Bullet Spawn")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("arial", 36)
small_font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 62, bold=True)

# Colors
SKY = (135, 206, 235)
GROUND = (34, 139, 34)
BOX_COLOR = (139, 69, 19)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)

# 5 maps (unchanged)
map_list = [
    [pygame.Rect(250, 90, 40, 200), pygame.Rect(250, 360, 40, 200),
     pygame.Rect(420, 200, 200, 40), pygame.Rect(680, 90, 40, 240),
     pygame.Rect(100, 240, 130, 40)],
    [pygame.Rect(300, 140, 380, 35), pygame.Rect(300, 470, 380, 35),
     pygame.Rect(200, 210, 35, 220), pygame.Rect(750, 210, 35, 220),
     pygame.Rect(420, 260, 160, 130)],
    [pygame.Rect(150, 80, 65, 340), pygame.Rect(780, 80, 65, 340),
     pygame.Rect(270, 160, 480, 45), pygame.Rect(270, 445, 480, 45),
     pygame.Rect(370, 260, 45, 130), pygame.Rect(580, 260, 45, 130)],
    [pygame.Rect(110, 100, 100, 100), pygame.Rect(220, 440, 100, 100),
     pygame.Rect(430, 150, 100, 100), pygame.Rect(640, 390, 100, 100),
     pygame.Rect(800, 210, 100, 100), pygame.Rect(310, 310, 200, 45)],
    [pygame.Rect(150, 150, 700, 35), pygame.Rect(150, 465, 700, 35),
     pygame.Rect(310, 210, 35, 240), pygame.Rect(655, 210, 35, 240),
     pygame.Rect(90, 300, 130, 45), pygame.Rect(780, 300, 130, 45)],
]

class Bullet:
    def __init__(self, x, y, angle, owner):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 9
        self.radius = 6
        self.owner = owner

    def update(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 215, 0), (int(self.x), int(self.y)), self.radius)

class Tank:
    def __init__(self, x, y, angle, color, player_num):
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color
        self.player_num = player_num
        self.health = 100
        self.ammo = 5
        self.max_ammo = 7
        self.speed = 3.8
        self.rot_speed = 3.8
        self.last_regen = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.surf = self.create_tank_surface()

    def create_tank_surface(self):
        surf = pygame.Surface((74, 48), pygame.SRCALPHA)
        pygame.draw.rect(surf, (50, 50, 50), (4, 5, 66, 13))
        pygame.draw.rect(surf, (50, 50, 50), (4, 30, 66, 13))
        pygame.draw.rect(surf, self.color, (12, 12, 50, 26))
        pygame.draw.circle(surf, self.color, (46, 25), 15)
        pygame.draw.rect(surf, BLACK, (52, 20, 28, 9))
        return surf

    def draw(self, screen):
        rotated = pygame.transform.rotate(self.surf, -self.angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        screen.blit(rotated, rect.topleft)

        bar_w = 66
        ratio = max(self.health, 0) / 100
        pygame.draw.rect(screen, (0, 0, 0), (self.x - bar_w//2, self.y - 48, bar_w, 9))
        pygame.draw.rect(screen, (0, 255, 0), (self.x - bar_w//2, self.y - 48, bar_w * ratio, 9))

    def move(self, forward, obstacles, other_tank=None):
        dx = math.cos(math.radians(self.angle)) * self.speed
        dy = math.sin(math.radians(self.angle)) * self.speed
        if not forward:
            dx = -dx
            dy = -dy
        new_x = self.x + dx
        new_y = self.y + dy

        tank_rect = pygame.Rect(new_x - 24, new_y - 16, 48, 32)

        if tank_rect.left < 15 or tank_rect.right > WIDTH - 15 or tank_rect.top < 15 or tank_rect.bottom > HEIGHT - 15:
            return

        for obs in obstacles:
            if tank_rect.colliderect(obs):
                return

        if other_tank:
            other_rect = pygame.Rect(other_tank.x - 24, other_tank.y - 16, 48, 32)
            if tank_rect.colliderect(other_rect):
                return

        self.x = new_x
        self.y = new_y

    def rotate(self, direction):
        self.angle = (self.angle + direction * self.rot_speed) % 360

    def update_ammo(self, game_start_time):
        now = pygame.time.get_ticks()
        elapsed = now - game_start_time
        interval = 1000 if elapsed < 5000 else 2000
        if now - self.last_regen > interval and self.ammo < self.max_ammo:
            self.ammo += 1
            self.last_regen = now

    def shoot(self, bullets_list):
        now = pygame.time.get_ticks()
        if (self.ammo > 0 and now - self.last_shot > 380 and
            len([b for b in bullets_list if b.owner == self.player_num]) < 5):
            # ==================== FIXED BULLET SPAWN ====================
            # Now spawns from the FRONT of the tank body (not the long barrel tip)
            # This fixes the problem when tanks are stuck together - bullet always hits!
            bx = self.x + math.cos(math.radians(self.angle)) * 34
            by = self.y + math.sin(math.radians(self.angle)) * 34
            bullets_list.append(Bullet(bx, by, self.angle, self.player_num))
            self.ammo -= 1
            self.last_shot = now

# ====================== GLOBAL VARIABLES ======================
tank1 = tank2 = None
bullets = []
obstacles = []
game_start_time = 0
two_player_mode = False
last_with_bot = True
paused = False
state = "main"
winner = None

def draw_button(text, rect, color):
    pygame.draw.rect(screen, color, rect, border_radius=15)
    pygame.draw.rect(screen, (0, 0, 0), rect, 5, border_radius=15)
    txt = font.render(text, True, WHITE)
    screen.blit(txt, txt.get_rect(center=rect.center))

def has_line_of_sight(attacker, target, obstacles):
    dx = target.x - attacker.x
    dy = target.y - attacker.y
    dist = math.hypot(dx, dy)
    if dist < 30: return True
    steps = max(8, int(dist / 9))
    for i in range(1, steps):
        px = attacker.x + dx * i / steps
        py = attacker.y + dy * i / steps
        if any(pygame.Rect(px-5, py-5, 10, 10).colliderect(obs) for obs in obstacles):
            return False
    return True

def find_safe_position(side, obstacles):
    if side == "left":
        x_range = range(100, 240)
    else:
        x_range = range(WIDTH - 240, WIDTH - 100)
    for _ in range(120):
        x = random.choice(list(x_range))
        y = random.randint(160, HEIGHT - 160)
        test_rect = pygame.Rect(x - 24, y - 16, 48, 32)
        if not any(test_rect.colliderect(obs) for obs in obstacles):
            return x, y
    return 160 if side == "left" else WIDTH - 160, HEIGHT // 2

def start_new_game(with_bot):
    global tank1, tank2, bullets, obstacles, game_start_time, two_player_mode, paused, winner, last_with_bot
    two_player_mode = not with_bot
    last_with_bot = with_bot
    paused = False
    winner = None
    bullets = []
    game_start_time = pygame.time.get_ticks()
    obstacles = random.choice(map_list)[:]

    x1, y1 = find_safe_position("left", obstacles)
    x2, y2 = find_safe_position("right", obstacles)
    tank1 = Tank(x1, y1, 0, RED, 1)
    tank2 = Tank(x2, y2, 180, BLUE, 2)
    
    # Slower, balanced AI tank
    if not two_player_mode:
        tank2.speed = 2.5
        tank2.rot_speed = 2.9

def ai_control(bot, target, obstacles, bullets_list):
    """ULTRA SMART AI - Smooth steering + real path calculation + bullet/wood dodging"""
    dx = target.x - bot.x
    dy = target.y - bot.y
    target_angle = math.degrees(math.atan2(dy, dx))
    dist = math.hypot(dx, dy)
    los = has_line_of_sight(bot, target, obstacles)

    # ==================== 1. HIGH PRIORITY: DODGE ENEMY BULLETS ====================
    dodge_angle = None
    for b in bullets_list:
        if b.owner != bot.player_num:
            bdx = b.x - bot.x
            bdy = b.y - bot.y
            bdist = math.hypot(bdx, bdy)
            if 12 < bdist < 145:
                dx_from_bullet_to_bot = bot.x - b.x
                dy_from_bullet_to_bot = bot.y - b.y
                dir_from_bullet = math.degrees(math.atan2(dy_from_bullet_to_bot, dx_from_bullet_to_bot))
                heading_diff = (dir_from_bullet - b.angle + 180) % 360 - 180
                if abs(heading_diff) < 37:
                    dodge_angle = (b.angle + (90 if random.random() < 0.5 else -90)) % 360
                    break

    if dodge_angle is not None:
        diff = (dodge_angle - bot.angle + 180) % 360 - 180
        bot.rotate(1 if diff > 0 else -1)
        bot.move(True, obstacles, target)
        return

    # ==================== 2. NORMAL AI BEHAVIOR ====================
    angle_diff = (target_angle - bot.angle + 180) % 360 - 180
    if abs(angle_diff) > 4:
        bot.rotate(1 if angle_diff > 0 else -1)

    if los and abs(angle_diff) < 11 and dist < 530 and random.random() < 0.068:
        bot.shoot(bullets_list)

    # ==================== 3. SMART PATH CALCULATION ====================
    if dist > 158:
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

                sim_rect = pygame.Rect(sim_x - 24, sim_y - 16, 48, 32)

                if (sim_rect.left < 15 or sim_rect.right > WIDTH - 15 or
                    sim_rect.top < 15 or sim_rect.bottom > HEIGHT - 15):
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

# ====================== MAIN LOOP ======================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            if screen.get_flags() & pygame.FULLSCREEN:
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
            else:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if state == "main":
                if 300 <= mx <= 700 and 220 <= my <= 290:
                    state = "submenu"
                if 300 <= mx <= 700 and 320 <= my <= 390:
                    running = False

            elif state == "submenu":
                if 300 <= mx <= 700 and 200 <= my <= 270:
                    start_new_game(True)
                    state = "game"
                if 300 <= mx <= 700 and 290 <= my <= 360:
                    start_new_game(False)
                    state = "game"
                if 300 <= mx <= 700 and 400 <= my <= 460:
                    state = "main"

            elif state == "game":
                pause_rect = pygame.Rect(WIDTH - 65, 15, 50, 50)
                if pause_rect.collidepoint(mx, my) and not paused:
                    paused = True
                elif paused:
                    resume_rect = pygame.Rect(WIDTH//2 - 160, 260, 320, 75)
                    menu_rect = pygame.Rect(WIDTH//2 - 160, 360, 320, 75)
                    if resume_rect.collidepoint(mx, my):
                        paused = False
                    elif menu_rect.collidepoint(mx, my):
                        state = "main"
                        paused = False
                        winner = None

            if winner:
                restart_rect = pygame.Rect(WIDTH//2 - 190, HEIGHT//2 + 70, 170, 70)
                menu_rect = pygame.Rect(WIDTH//2 + 30, HEIGHT//2 + 70, 170, 70)
                if restart_rect.collidepoint(mx, my):
                    start_new_game(last_with_bot)
                    state = "game"
                elif menu_rect.collidepoint(mx, my):
                    state = "main"
                    winner = None
                    paused = False

    keys = pygame.key.get_pressed()

    if state == "game" and not paused and winner is None:
        # ==================== PLAYER 1 (Red) ====================
        if keys[pygame.K_w]:
            tank1.angle = 270
            tank1.move(True, obstacles, tank2)
        if keys[pygame.K_s]:
            tank1.angle = 90
            tank1.move(True, obstacles, tank2)
        if keys[pygame.K_a]:
            tank1.angle = 180
            tank1.move(True, obstacles, tank2)
        if keys[pygame.K_d]:
            tank1.angle = 0
            tank1.move(True, obstacles, tank2)
        if keys[pygame.K_SPACE]:
            tank1.shoot(bullets)

        # ==================== PLAYER 2 (Blue) ====================
        if two_player_mode:
            if keys[pygame.K_UP]:
                tank2.angle = 270
                tank2.move(True, obstacles, tank1)
            if keys[pygame.K_DOWN]:
                tank2.angle = 90
                tank2.move(True, obstacles, tank1)
            if keys[pygame.K_LEFT]:
                tank2.angle = 180
                tank2.move(True, obstacles, tank1)
            if keys[pygame.K_RIGHT]:
                tank2.angle = 0
                tank2.move(True, obstacles, tank1)
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                tank2.shoot(bullets)
        else:
            ai_control(tank2, tank1, obstacles, bullets)

        tank1.update_ammo(game_start_time)
        tank2.update_ammo(game_start_time)

        # Bullets update + collision
        for b in bullets[:]:
            b.update()
            br = pygame.Rect(b.x - b.radius, b.y - b.radius, b.radius*2, b.radius*2)
            if not (0 < b.x < WIDTH and 0 < b.y < HEIGHT) or any(br.colliderect(o) for o in obstacles):
                bullets.remove(b)
                continue
            for t in (tank1, tank2):
                if t.player_num != b.owner:
                    tr = pygame.Rect(t.x - 24, t.y - 16, 48, 32)
                    if br.colliderect(tr):
                        t.health -= 34
                        if t.health <= 0:
                            winner = f"Player {b.owner} Wins!" if two_player_mode else ("YOU WIN!" if b.owner == 1 else "BOT Wins!")
                        bullets.remove(b)
                        break

    # ====================== DRAW ======================
    screen.fill(SKY)
    pygame.draw.rect(screen, GROUND, (0, HEIGHT - 85, WIDTH, 85))

    if state in ("game", "pause"):
        for obs in obstacles:
            pygame.draw.rect(screen, BOX_COLOR, obs)
            pygame.draw.rect(screen, (80, 40, 10), obs, 7)

        tank1.draw(screen)
        tank2.draw(screen)
        for b in bullets:
            b.draw(screen)

        # Ammo display
        pygame.draw.rect(screen, (30,30,30), (25, HEIGHT-62, 260, 48), border_radius=8)
        pygame.draw.rect(screen, WHITE, (25, HEIGHT-62, 260, 48), 4, border_radius=8)
        screen.blit(small_font.render(f"P1 Bullets: {tank1.ammo}/7", True, WHITE), (42, HEIGHT-53))

        pygame.draw.rect(screen, (30,30,30), (WIDTH-285, HEIGHT-62, 260, 48), border_radius=8)
        pygame.draw.rect(screen, WHITE, (WIDTH-285, HEIGHT-62, 260, 48), 4, border_radius=8)
        screen.blit(small_font.render(f"P2 Bullets: {tank2.ammo}/7", True, WHITE), (WIDTH-268, HEIGHT-53))

        pause_rect = pygame.Rect(WIDTH - 65, 15, 50, 50)
        pygame.draw.rect(screen, (230,230,230), pause_rect, border_radius=10)
        screen.blit(font.render("||", True, BLACK), (WIDTH - 54, 19))

    if state == "main":
        title = big_font.render("TANK BATTLE", True, (220, 20, 20))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 90))
        draw_button("PLAY", pygame.Rect(300, 220, 400, 70), (50, 160, 50))
        draw_button("EXIT", pygame.Rect(300, 320, 400, 70), (180, 40, 40))

    elif state == "submenu":
        screen.blit(small_font.render("Choose Mode", True, WHITE), (WIDTH//2 - 90, 120))
        draw_button("Play with Bot", pygame.Rect(300, 200, 400, 70), (40, 100, 200))
        draw_button("Play with Friend", pygame.Rect(300, 290, 400, 70), (40, 100, 200))
        draw_button("Back", pygame.Rect(300, 400, 400, 60), (140, 140, 140))

    if paused:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        screen.blit(font.render("PAUSED", True, WHITE), (WIDTH//2 - 85, 170))
        draw_button("RESUME", pygame.Rect(WIDTH//2 - 160, 260, 320, 75), (50, 160, 50))
        draw_button("MAIN MENU", pygame.Rect(WIDTH//2 - 160, 360, 320, 75), (180, 50, 50))

    if winner:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(170)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        win_text = big_font.render(winner, True, (255, 215, 0))
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 110))
        draw_button("RESTART", pygame.Rect(WIDTH//2 - 190, HEIGHT//2 + 70, 170, 70), (50, 160, 50))
        draw_button("MAIN MENU", pygame.Rect(WIDTH//2 + 30, HEIGHT//2 + 70, 170, 70), (180, 50, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()