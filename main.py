import math
import settings
import random
import pygame
import time
import pygame.font
import sys
import pygame.locals
from targetunit import *
from constants import *
from ballunit import *
from gununit import *

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






#----------класс пуля
class Bullet(Ball):
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        super().__init__(screen, x, y)
        self.r = 5  # Change the radius of the bullet
        self.color = BLACK  # Change the color of the bullet

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

    # Render the player's name in green with a font size of 48
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
    close_button, replay_button = display_endgame_statistics(screen, stats_font, settings.player)
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
                    settings.player.balls = 10

                    main_game_loop()
                    end_game_screen()


# ---------------- для перезапуска основного тела игры
def main_game_loop():
    finished = False
    gun = Gun(screen, speed=10)
    clock = pygame.time.Clock()
    bomb_timer = 0  # Add this line to create a timer for the bombs
    global game_over
    target = Target(screen)
    while not finished:

        screen.fill(WHITE)
        gun.draw()
        target.move()  # Call the move method for the target
        target.draw()
        for b in balls:
            b.draw()
        for b in bullets:
            b.move()
            b.draw()
        # Draw statistics on the screen
        draw_statistics(screen, stats_font, settings.player)

        if settings.player.balls == 0:
            finished = True

        for f in fragments:
            f.draw()
            f.move()
        # Add bomb creation
        bomb_timer += clock.get_time()
        if bomb_timer >= 5000:  # 5 seconds
            bomb = Bomb(screen)
            bombs.append(bomb)
            bomb_timer = 0
        # Draw and move bombs
        for b in bombs:
            b.draw()
            b.move()

        # Check bomb collisions
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
                settings.player.hits += 1
                settings.player.balls += random.randint(1, 3)
                if len(bullets)>1: bullets.remove(b)

        gun.power_up()

    end_game_screen()


# ----------------------------------------------------------тело игры
settings.init()
pygame.init()
pygame.font.init()  # Initialize the pygame.font module
stats_font = pygame.font.Font(None, 24)  # Move this line here
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# fragments = []

bombs = []
game_over = False
settings.player = Player("")  # Инициализируем игрока с пустым именем
player_name = settings.player.get_player_name(screen)
settings.player.name = player_name  # Задаем имя игрока

main_game_loop()

pygame.quit()
