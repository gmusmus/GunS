import math
from random import choice
import random
import pygame
import constants

import classball
import classgun
import classtarget

#global balls, bullet
#bullet = 0

def rnd(start, end):
    return random.randint(start, end)



pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
classgun.bullet = 0
classgun.balls = []

clock = pygame.time.Clock()
gun = classgun.Gun(screen)
target = classtarget.Target()
finished = False

while not finished:
    screen.fill(constants.WHITE)
    gun.draw()
    target.draw()
    for b in classgun.balls:
        b.draw()
    pygame.display.update()

    clock.tick(constants.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in classgun.balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
    gun.power_up()

pygame.quit()
