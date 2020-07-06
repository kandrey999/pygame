import pygame
from constants import *


class GameController:
    def __init__(self, player):
        self.player = player

    def handle_events(self):

        player = self.player

        # print(player.speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise ValueError('stop')
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            #     player.shoot()

        key_states = pygame.key.get_pressed()

        if key_states[pygame.K_SPACE]:
            player.shoot()

        player.speed = (0, 0)
        if key_states[pygame.K_LEFT]:
            player.speed = (-10, 0)
        elif key_states[pygame.K_RIGHT]:
            player.speed = (10, 0)
        elif key_states[pygame.K_UP]:
            player.speed = (0, -10)
        elif key_states[pygame.K_DOWN]:
            player.speed = (0, 10)

        player.rect.x += player.speed[0]
        player.rect.y += player.speed[1]

        if player.rect.right > WIDTH + 25:
            player.rect.right = WIDTH + 25
        elif player.rect.left < -25:
            player.rect.left = -25

        if player.rect.top < 0:
            player.rect.top = 0
        elif player.rect.bottom > HEIGHT and not player.hide:
            player.rect.bottom = HEIGHT
