import pygame
from pygame.sprite import Sprite
from constants import *
from random import randrange, choice, randint
from resources import rc
from collections import namedtuple

# import resources as rc
# from os import path

Point = namedtuple('Point', 'x y')
Size = namedtuple('Size', 'width height')


class Mob(Sprite):
    # img_names = ['meteorBrown_big1.png', 'meteorBrown_med1.png',
    #              'meteorGrey_big3.png', 'meteorGrey_med2.png']
    #
    # snd_names = ['expl3.wav', 'expl6.wav']

    def __init__(self, screen_size, *args):
        super().__init__(*args)
        self._screen_size = Size(*screen_size)
        self._groups = args
        # self.explosion_sounds = [rc.get_sound(name) for name in self.snd_names]
        # self.images = [rc.get_image_with_rect(name) for name in self.img_names]
        self._image = choice(rc.images['mob'])
        self.rect = self._image.get_rect()  # choice(self.images)
        self.image = self._image
        self.expl_sound = choice(rc.sounds['explosion'])
        self._speed = randrange(-10, 10), randrange(5, 15)
        self.radius = min(self.rect.width, self.rect.height) // 2
        self.rot = 0
        self.rot_speed = randrange(-3, 4)
        self.rect.topleft = randrange(self._screen_size.width - self.rect.width), \
                            randrange(-self.rect.height * 3, -self.rect.height)
        self.health = 100
        # pygame.draw.circle(self.image, RED, self.image.get_rect().center, self.radius)

    def rotate(self):
        self.rot = (self.rot + self.rot_speed) % 360
        self.image = pygame.transform.rotate(self._image, self.rot)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rotate()
        self.rect.move_ip(self._speed)
        if self.rect.top > self._screen_size.height + 10 or self.rect.right < -10 or \
                self.rect.left > self._screen_size.width + 10:
            # self.speed = randrange(-3, 4), randrange(1, 10)
            # self.rect.topleft = randrange(WIDTH - self.rect.width), \
            #                       randrange(-self.rect.height * 2, -self.rect.height)
            self.kill()
            # Mob(self._screen_size, self._groups)

    @property
    def explosion_sound(self):
        # return choice(self.explosion_sounds)
        return self.expl_sound
    # def __del__(self):
    #     print(f'del {self}')


class Bullet(Sprite):
    def __init__(self, start_pos):
        super().__init__()
        self.sound = rc.sounds['pew']  # rc.get_sound('pew.wav')
        self.image = rc.images['bullet']
        self.rect = self.image.get_rect()  # rc.get_image_with_rect('laserRed07.png')
        self.speed_y = -15
        self.rect.centerx, self.rect.bottom = start_pos
        self.sound.play()

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()


class ProgressBar(Sprite):
    def __init__(self, x, y, width=100, height=10, value=0, min_value=0, max_value=100):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self._value = value
        self.min_value = min_value
        self.max_value = max_value
        self._draw()

    def _draw(self):
        fill_width = self.value / (self.max_value - self.min_value) * self.rect.width
        fill_rect = pygame.Rect(0, 0, fill_width, self.rect.height)
        pygame.draw.rect(self.image, WHITE, pygame.Rect(0, 0, self.rect.width, self.rect.height))
        pygame.draw.rect(self.image, GREEN, fill_rect)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self._value != value:
            self._value = value
            self._draw()


class PlayerHealthProgressBar(ProgressBar):
    def __init__(self, player):
        super().__init__(10, 20)
        self._player = player

    def update(self):
        self.value = self._player.health


class TextLabel(Sprite):
    def __init__(self, pos, text='0', font_name='arial'):
        super().__init__()
        self._pos = pos
        self.font = pygame.font.Font(pygame.font.match_font(font_name), 20)
        self._text = text
        self._draw()

    def _draw(self):
        self.image = self.font.render(self._text, True, WHITE)
        self.rect = self.image.get_rect(topleft=self._pos)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)
        self._draw()


class AnimatedSprite(Sprite):
    def __init__(self, images, frame_rate, repeat=0):
        super().__init__()
        self._images = images
        self.image = self._images[0]
        self.rect = self.image.get_rect()
        # self.rect = self.image.get_rect(center=pos)
        self._frame_rate = frame_rate
        self._last_update = 0
        self._current_frame = 0
        self._repeat = repeat

    def update(self):
        now = pygame.time.get_ticks()
        if now - self._last_update > self._frame_rate:
            self._last_update = now
            self._current_frame += 1
            if self._current_frame == len(self._images):
                if not self._repeat:
                    self.kill()
                else:
                    self._repeat -= 1
            else:
                self.image = self._images[self._current_frame]
                self.rect = self.image.get_rect()


class AbstractExplosion(AnimatedSprite):
    def __init__(self, pos, images, frame_rate):
        super().__init__(images, frame_rate)
        self._pos = pos

    def update(self):
        super().update()
        self.rect.center = self._pos


class Explosion(AbstractExplosion):
    def __init__(self, pos, size):
        images = [pygame.transform.scale(image, (size, size)) for image in rc.images['explosion']]
        # images = [rc.get_scaled_image(path.join('regularExplosions', f'regularExplosion0{i}.png'),
        #                               (size, size)) for i in range(9)]
        super().__init__(pos, images, 10)


class PlayerExplosion(AbstractExplosion):
    def __init__(self, pos):
        images = rc.images['player_explosion']
        # self.images = [rc.get_image(path.join('sonicExplosions', f'sonicExplosion0{i}.png')) for i in range(9)]
        super().__init__(pos, images, 20)


class ImageProgressBar(Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        # self.image = pygame.Surface((lives * 30, 50))
        # self.image.set_colorkey(BLACK)
        # self.image = img
        # self.rect = self.image.get_rect(right=x, top=y)
        self._x, self._y = x, y
        self._image = image
        self._value = 0
        self._draw(self._value)

    def _draw(self, value):
        # self.image.fill(BLACK)
        rect = self._image.get_rect()
        self.image = pygame.Surface((value * rect.width * 1.2, rect.height * 2))
        self.rect = self.image.get_rect(right=self._x, top=self._y)
        self.image.set_colorkey(BLACK)
        for i in range(value):
            img_rect = self._image.get_rect()
            img_rect.x = rect.width * i * 1.2
            img_rect.y = 10
            self.image.blit(self._image, img_rect)
            # screen.blit(self.image, img_rect)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self._value != value:
            print('set')
            self._value = value
            self._draw(self._value)
        # print('set')
        # self._value = value
        # self._draw(self._value)


class PlayerLivesProgressBar(ImageProgressBar):
    def __init__(self, x, y, player):
        self.image = pygame.transform.scale(rc.images['player'],
                                            (20, 20))  # rc.get_scaled_image('playerShip1_orange.png', (20, 20))
        super().__init__(x, y, self.image)
        self._player = player

    def update(self):
        self.value = self._player.lives


class Bonus(Sprite):
    # names = ['bolt_gold.png', 'shield_gold.png']

    def __init__(self, pos, height):
        super().__init__()
        self._height = height
        self._type = randint(0, 1)
        self._image = rc.images['bonuses'][self._type]  # rc.get_image(self.names[self._type])
        self._rect = self.image.get_rect(center=pos)
        self.speed_y = 3

    @property
    def type(self):
        return self._type

    @property
    def image(self):
        return self._image

    @property
    def rect(self):
        return self._rect

    def update(self):
        self._rect.y += self.speed_y
        if self._rect.top > self._height:
            self.kill()


class GunPowerImageProgressBar(ImageProgressBar):
    def __init__(self, x, y, player):
        self.image = rc.images['bonus_bolt_small']  # rc.get_scaled_image('bolt_gold.png', (20, 20))
        super().__init__(x, y, self.image)
        self.player = player

    def update(self):
        self.value = self.player.power

# class SonicExplosion(AbstractExplosion):
#     def __init__(self, pos, size):
#         self.anims = []
#         self.current_frame = 0
#         self.frame_rate =
#         self.last_update =


# class AbstractExplosion(Sprite):
#     def __init__(self, pos, size):
#         super().__init__()
#         self.size = size

# self.rect = self.image.get_rect(center=self.rect.center)


# class Explosion(AbstractExplosion):
#     def __init__(self, pos, size):
#         self.anims = [rc.get_scaled_image(path.join('regularExplosions', f'regularExplosion0{i}.png'),
#                                           (size, size)) for i in range(9)]
#         super().__init__(pos, size)
