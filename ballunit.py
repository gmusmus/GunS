# Разработчик модуля Антон
import pygame
import random
import math
from targetunit import *
from constants import *

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
