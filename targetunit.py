# Разработчик модуля Дмитрий
import pygame
import random
import math
from constants import *

# -----------------------класс распадающей цели
class Fragment:  #содержит свойства и методы для создания и управления фрагментами на экране. Инициализируются свойства экрана, координаты, цвет, размер,
                 # скорость кроме того, определяется время жизни фрагментов в кадрах.
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

    def move(self): # метод move() класса Fragment - перемещает фрагмент на экране, изменяя его координаты (x и y) в соответствии со скоростью (vx и vy),
                    # гравитацией и сопротивлением воздуха. Если фрагмент достигает нижней границы экрана (если его координата y + размер фрагмента превышает
                    # высоту экрана), то его скорость по вертикали меняется на противоположную, уменьшенную на 60%, а по горизонтали скорость уменьшается на 40%.
                    # Если время жизни фрагмента истекает (life == 0), то фрагмент удаляется из списка фрагментов.
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

    def hittest(self, obj):  # Метод определяет растояние от снаряда до цели.
        gun_center_x = obj.gun_rect.x + obj.gun_rect.width // 2
        gun_center_y = obj.gun_rect.y + obj.gun_rect.height // 2
        distance = math.sqrt((self.x - gun_center_x) ** 2 + (self.y - gun_center_y) ** 2)
        fragment_radius = self.size // 2
        return distance <= fragment_radius + obj.gun_rect.height // 2
# -----------------------класс цели
class Target:
    def __init__(self, screen: pygame.Surface):  # Добавление параметров экрана, счетчика очков и количества жизней
        self.screen = screen
        self.points = 0
        self.live = 1
        self.new_target()

    def new_target(self): #Создает новую мишень
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 550)
        self.r = random.randint(10, 45)
        self.color = RED
        self.vx = random.uniform(-2, 2)  # Обеспечивает движение мишени
        self.vy = random.uniform(-2, 2)
        self.live = 1  #сбрасывает количество жизней

    def move(self):
        self.x += self.vx
        self.y += self.vy

        # Проверяет цель - находится ли на краю экрана
        if self.x - self.r < 0 or self.x + self.r > WIDTH:
            self.vx = -self.vx
        if self.y - self.r < 0 or self.y + self.r > HEIGHT:
            self.vy = -self.vy

    def hit(self, points=1): #Считает очки за попадание в цель
        self.points += points

    def draw(self): #Рисует мишень
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def destroy(self):#Разрушение цели после попадания
        num_fragments = random.randint(10, 30)
        for i in range(num_fragments):
            fragment = Fragment(self.screen, self.x, self.y, self.color)
            fragments.append(fragment)
        self.live = 0
        self.points += 1
        self.new_target()


