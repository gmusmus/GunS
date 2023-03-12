# import math
# from random import choice
# import random
import pygame
from constants import *

# import classball
import classgun
import classtarget

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
classgun.bullet = 0
classgun.balls = []

clock = pygame.time.Clock()
gun = classgun.Gun(screen)
target = classtarget.Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in classgun.balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                gun.stepleft()
            elif event.key == pygame.K_d:
                gun.stepright()

    for b in classgun.balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
    gun.power_up()

pygame.quit()
