# Разработчик модуля Владимир
import pygame
import random
import math
from targetunit import *
from constants import *
from ballunit import *
import settings


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
        settings.player.shots += 1
        settings.player.balls -= 1

    def fire_bullet(self, event):
        global bullets, player
        new_bullet = Bullet(self.screen, self.gun_rect.x, self.gun_rect.y)
        self.an = math.atan2((self.gun_rect.y - event.pos[1]), (event.pos[0] - self.gun_rect.x))
        new_bullet.vx = 20 * math.cos(self.an)
        new_bullet.vy = -20 * math.sin(self.an)
        bullets.append(new_bullet)
        settings.player.shots += 1
        settings.player.balls -= 1

    def targetting(self, event):
        if event:
            self.an = math.atan2((self.gun_rect.y - event.pos[1]),
                                 (event.pos[0] - self.gun_rect.x))  # Используйте atan2
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY
