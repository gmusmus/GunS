import math
import random
import pygame
import time
import pygame.font
import sys
import pygame.locals

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 900
HEIGHT = 600


# -----------------------класс игрока
class Player:
    def __init__(self, name):
        self.name = name
        self.start_time = time.time()
        self.shots = 0
        self.hits = 0
        self.balls = 10

    def get_statistics(self):
        total_time = int(time.time() - self.start_time)
        hit_percent = self.hits / self.shots * 100 if self.shots > 0 else 0
        miss_percent = 100 - hit_percent
        return total_time, self.shots, self.hits, hit_percent, miss_percent

    def get_player_name(self, screen):
        font = pygame.font.Font(None, 36)
        input_box = pygame.Rect(300, 300, 200, 50)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = 'Noname'
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            screen.fill(WHITE)
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)
            pygame.display.flip()

        return text


# -----------------------класс распадающей цели
class Fragment:
    def __init__(self, screen, x, y, color):
        self.screen = screen
        self.x = x
        self.y = y
        self.color = color
        self.size = 5
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.gravity = 0.5
        self.air_resistance = 0.99
        self.life = 150

    def move(self):
        self.x += self.vx
        self.y += self.vy + self.gravity
        self.vx *= self.air_resistance
        self.vy *= self.air_resistance
        self.vy += self.gravity
        if self.y + self.size > HEIGHT:
            self.vy = -abs(self.vy) * 0.6
            self.vx *= 0.6
            self.y = HEIGHT - self.size
            self.life -= 1
        if self.life == 0:
            fragments.remove(self)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.size, self.size))

    def hittest(self, obj):
        gun_center_x = obj.gun_rect.x + obj.gun_rect.width // 2
        gun_center_y = obj.gun_rect.y + obj.gun_rect.height // 2
        distance = math.sqrt((self.x - gun_center_x) ** 2 + (self.y - gun_center_y) ** 2)
        fragment_radius = self.size // 2
        return distance <= fragment_radius + obj.gun_rect.height // 2

# -----------------------класс мяча
class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = random.choice(GAME_COLORS)
        self.live = 30
        self.wind = (0, 0)
        self.air_resistance = 0.99
        self.gravity = 0.5

    def move(self):
        self.x += self.vx + self.wind[0]
        self.y += self.vy + self.gravity + self.wind[1]
        self.vx *= self.air_resistance
        self.vy *= self.air_resistance
        self.vy += self.gravity
        if self.x - self.r < 0:
            self.vx = abs(self.vx)
        if self.x + self.r > WIDTH:
            self.vx = -abs(self.vx)
        if self.y + self.r > HEIGHT:
            self.vy = -abs(self.vy)
            self.y = HEIGHT - self.r  # мяч не может провалиться ниже нижней границы
            self.vy *= 0.6  # коэффициент затухания энергии от удара о поверхность
            if abs(self.vy) < 2:  # если скорость мала, мяч прекращает движение
                self.vy = 0
                self.vx = 0
                self.live -= 1
                if self.live == 0 and self in balls:
                    balls.remove(self)  # мяч исчезает
        if self.y - self.r < 0:
            self.vy = abs(self.vy)

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        distance = math.sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)
        return distance <= self.r + obj.r

    def destroy(self):
        num_fragments = random.randint(10, 30)
        for i in range(num_fragments):
            fragment = Fragment(self.screen, self.x, self.y, self.color)
            fragments.append(fragment)
        balls.remove(self)


# -----------------------класс пушки
class Gun:
    def __init__(self, screen, speed=5):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.speed = speed
        self.gun_rect = pygame.Rect(20, 450, 40, 10)
        self.width = 40
        self.height = 20
        self.gun_rect = pygame.Rect(20, 450, self.width, self.height)
        self.color = GREY
        self.speed = speed
        self.barrel_width = 10
        self.barrel_length = 50

    def fire2_start(self, event):
        self.f2_on = 1

    def move_up(self):
        self.gun_rect.y -= self.speed
        if self.gun_rect.y < 0:
            self.gun_rect.y = 0

    def move_down(self):
        self.gun_rect.y += self.speed
        if self.gun_rect.y > HEIGHT - self.gun_rect.height:
            self.gun_rect.y = HEIGHT - self.gun_rect.height

    def move_left(self):
        self.gun_rect.x -= self.speed
        if self.gun_rect.x < 0:
            self.gun_rect.x = 0

    def move_right(self):
        self.gun_rect.x += self.speed
        if self.gun_rect.x > WIDTH - self.gun_rect.width:
            self.gun_rect.x = WIDTH - self.gun_rect.width

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.gun_rect)

        barrel_start = (
            int(self.gun_rect.x + self.width / 2),
            int(self.gun_rect.y + self.height / 2),
        )
        barrel_end = (
            int(barrel_start[0] + self.barrel_length * math.cos(self.an)),
            int(barrel_start[1] - self.barrel_length * math.sin(self.an)),
        )
        pygame.draw.line(self.screen, self.color, barrel_start, barrel_end, self.barrel_width)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    def fire2_end(self, event):
        global balls, bullet, player
        bullet += 1
        new_ball = Ball(self.screen, self.gun_rect.x, self.gun_rect.y)
        new_ball.r += 5
        self.an = math.atan2((self.gun_rect.y - event.pos[1]), (event.pos[0] - self.gun_rect.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10
        player.shots += 1
        player.balls -= 1

    def fire_bullet(self, event):
        global bullets, player
        new_bullet = Bullet(self.screen, self.gun_rect.x, self.gun_rect.y)
        self.an = math.atan2((self.gun_rect.y - event.pos[1]), (event.pos[0] - self.gun_rect.x))
        new_bullet.vx = 20 * math.cos(self.an)
        new_bullet.vy = -20 * math.sin(self.an)
        bullets.append(new_bullet)
        player.shots += 1
        player.balls -= 1

    def targetting(self, event):
        if event:
            self.an = math.atan2((self.gun_rect.y - event.pos[1]),
                                 (event.pos[0] - self.gun_rect.x))  # Используйте atan2
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

#----------класс пуля
class Bullet(Ball):
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        super().__init__(screen, x, y)
        self.r = 5  
        self.color = BLACK  

    def hittest(self, obj):
        distance = math.sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)
        return distance <= self.r + obj.r


    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, 2 * self.r, self.r))

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if (
            self.x < 0
            or self.x > WIDTH
            or self.y < 0
            or self.y > HEIGHT
        ):
            bullets.remove(self)

# -----------------------класс цели

class Target:
    def __init__(self, screen: pygame.Surface): 
        self.screen = screen 
        self.points = 0
        self.live = 1
        self.new_target()

    def new_target(self):
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 550)
        self.r = random.randint(10, 45)
        self.color = RED
        self.vx = random.uniform(-2, 2)  
        self.vy = random.uniform(-2, 2)  
        self.live = 1 

    def move(self):
        self.x += self.vx
        self.y += self.vy


        if self.x - self.r < 0 or self.x + self.r > WIDTH:
            self.vx = -self.vx
        if self.y - self.r < 0 or self.y + self.r > HEIGHT:
            self.vy = -self.vy

    def hit(self, points=1):
        self.points += points

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def destroy(self):
        num_fragments = random.randint(10, 30)
        for i in range(num_fragments):
            fragment = Fragment(self.screen, self.x, self.y, self.color)
            fragments.append(fragment)
        self.live = 0
        self.points += 1
        self.new_target()

#--------------класс бомб
class Bomb:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.x = random.randint(0, WIDTH)
        self.y = 0
        self.r = 10
        self.color = BLACK
        self.vy = 2

    def move(self):
        self.y += self.vy
        if self.y + self.r > HEIGHT:
            self.explode()

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        if isinstance(obj, Gun):
            gun_center_x = obj.gun_rect.x + obj.gun_rect.width / 2
            gun_center_y = obj.gun_rect.y + obj.gun_rect.height / 2
            distance = math.sqrt((self.x - gun_center_x) ** 2 + (self.y - gun_center_y) ** 2)
            return distance <= self.r + max(obj.gun_rect.width, obj.gun_rect.height) / 2
        else:
            distance = math.sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)
            return distance <= self.r + obj.rц

    def explode(self):
        num_fragments = random.randint(10, 30)
        for i in range(num_fragments):
            fragment = Fragment(self.screen, self.x, self.y, random.choice(GAME_COLORS))
            fragments.append(fragment)
        bombs.remove(self)


# -----------------------функции
def draw_statistics(screen, font, player):
    total_time, shots, hits, hit_percent, miss_percent = player.get_statistics()
    stats_text = (
        f"Время игры: {total_time} s | "
        f"Выстрелов: {shots} | "
        f"Попаданий: {hits} ({hit_percent:.2f}%) | "
        f"Мимо: {shots - hits} ({miss_percent:.2f}%) | "
        f"Мячей: {player.balls} "
    )
    stats_surface = font.render(stats_text, True, BLACK)
    screen.blit(stats_surface, (10, 10))


    name_font = pygame.font.Font(None, 48)
    name_color = GREEN
    name_text = player.name
    name_surface = name_font.render(name_text, True, name_color)
    name_x = WIDTH - name_surface.get_width() - 10
    name_y = 10
    screen.blit(name_surface, (name_x, name_y))


def display_endgame_statistics(screen, font, player):
    endgame_font = pygame.font.Font(None, 36)
    total_time, shots, hits, hit_percent, miss_percent = player.get_statistics()
    stats_labels = [
        f"Игрок:",
        f"Время игры:",
        f"Выстрелов:",
        f"Попаданий:",
        f"Мимо:"
    ]
    stats_values = [
        f"{player.name}",
        f"{total_time} сек",
        f"{shots}",
        f"{hits} ({hit_percent:.2f}%)",
        f"{shots - hits} ({miss_percent:.2f}%)"
    ]

    stats_y_offset = 0
    for label, value in zip(stats_labels, stats_values):
        label_surface = endgame_font.render(label, True, BLACK)
        value_surface = endgame_font.render(value, True, BLACK)
        screen.blit(label_surface, (WIDTH // 2 - 150, HEIGHT // 2 - 100 + stats_y_offset))
        screen.blit(value_surface, (WIDTH // 2 + 50, HEIGHT // 2 - 100 + stats_y_offset))
        stats_y_offset += 40

    close_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 80, 40)
    close_text = font.render("Закрыть", True, BLACK)
    pygame.draw.rect(screen, GREY, close_button)
    screen.blit(close_text, (close_button.x + 10, close_button.y + 10))

    replay_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 100, 100, 40)
    replay_text = font.render("Переиграть", True, BLACK)
    pygame.draw.rect(screen, GREY, replay_button)
    screen.blit(replay_text, (replay_button.x + 10, replay_button.y + 10))

    pygame.display.flip()

    return close_button, replay_button


def end_game_screen():
    screen.fill(WHITE)
    close_button, replay_button = display_endgame_statistics(screen, stats_font, player)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif replay_button.collidepoint(event.pos):
                    player.balls = 10

                    main_game_loop()
                    end_game_screen()


# ---------------- для перезапуска основного тела игры
def main_game_loop():
    finished = False
    gun = Gun(screen, speed=10)
    clock = pygame.time.Clock()
    bomb_timer = 0  # таймер бомбы
    global game_over
    target = Target(screen)
    while not finished:

        screen.fill(WHITE)
        gun.draw()
        target.move()  # смещение цели по которой стреляем
        target.draw()
        for b in balls:
            b.draw()
        for b in bullets:
            b.move()
            b.draw()
        # статистику на экран выведем
        draw_statistics(screen, stats_font, player)

        if player.balls == 0:
            finished = True

        for f in fragments:
            f.draw()
            f.move()
        # создадим бомбочки
        bomb_timer += clock.get_time()
        if bomb_timer >= 5000:  # каждые 5 сек будут падать бомбы сверху
            bomb = Bomb(screen)
            bombs.append(bomb)
            bomb_timer = 0
        # нарисуем бомбочки
        for b in bombs:
            b.draw()
            b.move()

        
        for b in bombs:
            if b.hittest(gun):
                game_over = True
                break
            for f in fragments:
                if f.hittest(gun):
                    game_over = True
                    break
        if game_over:
            break
        pygame.display.update()

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.locals.BUTTON_LEFT:
                    gun.fire2_start(event)
                elif event.button == pygame.locals.BUTTON_RIGHT:
                    bullet = Bullet(screen, gun.gun_rect.x, gun.gun_rect.y)
                    bullet.vx = gun.f2_power * math.cos(gun.an)
                    bullet.vy = - gun.f2_power * math.sin(gun.an)
                    bullets.append(bullet)
            elif event.type == pygame.MOUSEBUTTONUP:
                gun.fire2_end(event)
            elif event.type == pygame.MOUSEMOTION:
                gun.targetting(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    gun.move_up()
                elif event.key == pygame.K_s:
                    gun.move_down()
                elif event.key == pygame.K_a:
                    gun.move_left()
                elif event.key == pygame.K_d:
                    gun.move_right()
                elif event.key == pygame.K_ESCAPE:
                    finished = True

        for b in balls:
            b.move()
            if b.hittest(target) and target.live:
                b.destroy()
                target.destroy()
                player.hits += 1
                player.balls += random.randint(1, 3)
                if len(bullets)>1: bullets.remove(b)

        gun.power_up()

    end_game_screen()


# ----------------------------------------------------------тело игры
pygame.init()
pygame.font.init()  
stats_font = pygame.font.Font(None, 24)  
screen = pygame.display.set_mode((WIDTH, HEIGHT))

bullet = 0
balls = []
fragments = [] 
bullets = []
bombs = []
game_over = False

player = Player("")  
player_name = player.get_player_name(screen)  
player.name = player_name  

main_game_loop()

pygame.quit()
