import math
# from random import choice
# import random
import pygame
from constants import *
import classball


# print(windll.user32.GetSystemMetrics(0))
# print(windll.user32.GetSystemMetrics(1))

class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x0 = 20 # Положение пушки по координате x
        self.y0 = 450 # Положение пушки по координате y
        self.calibr = 7 # Ширина ствола
        self.d_stvol = 20 # Длина ствола

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = classball.Ball(self.screen, self.x0, self.y0)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-self.y0) / (event.pos[0]-self.x0))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(self.screen, self.color, (self.x0, self.y0 ), (int(self.x0 + max(self.f2_power, self.d_stvol) *
            math.cos(self.an)), int(self.y0  + max(self.f2_power, self.d_stvol) * math.sin(self.an))), self.calibr)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY
    def stepleft(self):
        if self.x0 > 5:
            self.x0 -= 5
            self.draw()
    def stepright(self):
        if self.x0 <55:
            self.x0 += 5
            self.draw()
