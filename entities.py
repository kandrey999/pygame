import pygame
from pygame.sprite import Sprite, Group
from constants import *
from random import randrange, choice
import resources as rc
from os import path


class Player(Sprite):
    def __init__(self, init_pos):
        super().__init__()
        self._image = rc.get_image('playerShip1_orange.png')
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = init_pos
        self._radius = min(self.rect.width, self.rect.height) // 2
        self.speed = (0, 0)
        self._shoot_rate = 100  # ms
        self._hidden = False
        self.lives = 5
        self._hide_time = 0
        self._last_update = pygame.time.get_ticks()
        # pygame.draw.circle(self.image, RED, self.image.get_rect().center, self.radius)

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
            self._last_update = now
            bullet = Bullet((self.rect.centerx, self.rect.top))
            all_sprites.add(bullet)
            bullets.add(bullet)

    def hide(self):
        self._hidden = True
        self.rect.y = 5000
        self._hide_time = pygame.time.get_ticks()

    def show(self):
        self._hidden = False
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10


class Mob(Sprite):
    img_names = ['meteorBrown_big1.png', 'meteorBrown_med1.png',
                 'meteorGrey_big3.png', 'meteorGrey_med2.png']
    images = [rc.get_image_with_rect(name) for name in img_names]

    snd_names = ['expl3.wav', 'expl6.wav']
    explosion_sounds = [rc.get_sound(name) for name in snd_names]

    def __init__(self, *args):
        super().__init__(*args)
        self._image, self.rect = choice(Mob.images)
        self.image = self._image
        self._speed = randrange(-10, 10), randrange(5, 15)
        self.radius = min(self.rect.width, self.rect.height) // 2
        self.rot = 0
        self.rot_speed = randrange(-3, 4)
        self.rect.topleft = randrange(WIDTH - self.rect.width), \
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
        if self.rect.top > HEIGHT + 10 or self.rect.right < -10 or self.rect.left > WIDTH + 10:
            # self.speed = randrange(-3, 4), randrange(1, 10)
            # self.rect.topleft = randrange(WIDTH - self.rect.width), \
            #                       randrange(-self.rect.height * 2, -self.rect.height)
            self.kill()
            Mob(all_sprites, mobs)

    @property
    def explosion_sound(self):
        return choice(Mob.explosion_sounds)

    # def __del__(self):
    #     print(f'del {self}')


class Bullet(Sprite):
    sound = rc.get_sound('pew.wav')

    def __init__(self, start_pos):
        super().__init__()
        self.image, self.rect = rc.get_image_with_rect('laserRed07.png')
        self.speed_y = -10
        self.rect.centerx, self.rect.bottom = start_pos
        Bullet.sound.play()

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
        self._value = value
        self._draw()


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
        images = [rc.get_scaled_image(path.join('regularExplosions', f'regularExplosion0{i}.png'),
                                      (size, size)) for i in range(9)]
        super().__init__(pos, images, 10)


class PlayerExplosion(AbstractExplosion):
    images = [rc.get_image(path.join('sonicExplosions', f'sonicExplosion0{i}.png')) for i in range(9)]

    def __init__(self, pos):
        super().__init__(pos, self.images, 20)


class ImageProgressBar(Sprite):
    def __init__(self, x, y, lives, image):
        super().__init__()
        # self.image = pygame.Surface((lives * 30, 50))
        # self.image.set_colorkey(BLACK)
        # self.image = img
        # self.rect = self.image.get_rect(right=x, top=y)
        self.x = x
        self.y = y
        self._image = image
        self._value = lives
        self._draw(self._value)

    def _draw(self, value):
        # self.image.fill(BLACK)
        rect = self._image.get_rect()
        self.image = pygame.Surface((value * rect.width, rect.height * 2))
        self.rect = self.image.get_rect(right=self.x, top=self.y)
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
        # print('set')
        self._value = value
        self._draw(self._value)


class PlayerHealthProgressBar(ImageProgressBar):
    image = rc.get_scaled_image('playerShip1_orange.png', (40, 40))

    def __init__(self, x, y, lives):
        super().__init__(x, y, lives, self.image)


class Bonus(Sprite):
    names = ['bold_gold.png', 'shield_gold.png']

    def __init__(self, pos):
        super().__init__()
        self._image = rc.get_image(choice(Bonus.names))
        self._rect = self.image.get_rect(center=pos)
        self.speed_y = 3

    @property
    def image(self):
        return self._image

    @property
    def rect(self):
        return self._rect

    def update(self):
        self._rect.y += self.speed_y
        if self._rect.top > HEIGHT:
            self.kill()


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


all_sprites = Group()
player = Player((WIDTH / 2, HEIGHT - 10))
all_sprites.add(player)
mobs = Group()
bullets = Group()
for i in range(MOB_COUNT):
    mob = Mob(all_sprites, mobs)

progress_bar = ProgressBar(10, 10, value=100, height=15)
all_sprites.add(progress_bar)

score = TextLabel((WIDTH / 2, 10))
all_sprites.add(score)

player_health_bar = PlayerHealthProgressBar(WIDTH - 10, 0, player.lives)
all_sprites.add(player_health_bar)
