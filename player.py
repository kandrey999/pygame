import pygame
from pygame.sprite import Sprite
from random import randrange
from resources import rc
from entities import Bullet


# import resources as rc
# from entities import Bullet
# rc.get_image('playerShip1_orange.png')

class Player(Sprite):
    def __init__(self, init_pos, all_sprites, bullets):
        super().__init__()
        self._init_pos = init_pos
        self._all_sprites = all_sprites
        self._bullets = bullets
        self._image = rc.images['player']
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = init_pos
        self._radius = min(self.rect.width, self.rect.height) // 2
        self._speed = (0, 0)
        self._shoot_rate = 100  # ms
        self._hidden = False
        self._lives = 3
        self._health = 100
        self._hide_time = 0
        self._power = 0
        self._power_time = 0
        self._shoot_power_time = 5000  # ms
        # self._bullet = bullet
        self._last_update = pygame.time.get_ticks()
        # pygame.draw.circle(self.image, RED, self.image.get_rect().center, self.radius)

    @property
    def power(self):
        return self._power

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value):
        self._lives = value

    @property
    def health(self):
        return self._health

    @property
    def image(self):
        return self._image

    @property
    def radius(self):
        return self._radius

    @property
    def hide_time(self):
        return self._hide_time

    @property
    def hidden(self):
        return self._hidden

    def move(self, key_states):
        self._speed = (0, 0)
        if key_states[pygame.K_RIGHT]:
            self._speed = (10, self._speed[1])
        elif key_states[pygame.K_LEFT]:
            self._speed = (-10, self._speed[1])
        if key_states[pygame.K_UP]:
            self._speed = (self._speed[0], -10)
        elif key_states[pygame.K_DOWN]:
            self._speed = (self._speed[0], 10)

        self.rect.x += self._speed[0]
        self.rect.y += self._speed[1]

        if key_states[pygame.K_SPACE]:
            self.shoot()

    def check_borders(self, size):
        if self.rect.right > size[0] + 25:
            self.rect.right = size[0] + 25
        elif self.rect.left < -25:
            self.rect.left = -25
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > size[1] and not self._hidden:
            self.rect.bottom = size[1]

    def update2(self, key_states, size):
        self.move(key_states)
        self.check_borders(size)

        if self._health > 100:
            self._health = 100
        now = pygame.time.get_ticks()
        if self._power >= 1 and now - self._power_time >= self._shoot_power_time:
            self._power -= 1
            self._power_time = now

    def on_catch_bonus(self, bonus):
        if bonus.type == 1:
            self._health += randrange(30, 50)
        elif bonus.type == 0:
            self._power += 1
            self._power_time = pygame.time.get_ticks()

    def on_destroy(self):
        self._lives -= 1
        self._health = 100

    def on_damage(self, damage):
        self._health -= damage

    # @property
    # def lives(self):
    #     return self._lives
    # @lives.setter
    # def lives(self, value):
    #     self._lives += value
    #     if self._lives > 10:
    #         self._lives = 10

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self._last_update > self._shoot_rate:
            if self.power == 0:
                self._last_update = now
                bullet = Bullet((self.rect.centerx, self.rect.top))
                self._all_sprites.add(bullet)
                self._bullets.add(bullet)
            if self.power >= 1:
                self._last_update = now
                left_bullet = Bullet((self.rect.left, self.rect.centery))
                right_bullet = Bullet((self.rect.right, self.rect.centery))
                self._all_sprites.add(left_bullet, right_bullet)
                self._bullets.add(left_bullet, right_bullet)

    def hide(self):
        self._hidden = True
        self.rect.y = 5000
        self._hide_time = pygame.time.get_ticks()

    def show(self):
        self._hidden = False
        self.rect.centerx, self.rect.bottom = self._init_pos
