import os
import pygame


class Resources:
    def __init__(self):
        self.dir_name = os.path.dirname(__file__)
        self.img_dir = os.path.join(self.dir_name, 'arts')
        self.snd_dir = os.path.join(self.dir_name, 'sounds')
        self.images = dict()
        self.sounds = dict()

    def _load_image(self, name):
        img_path = os.path.join(self.img_dir, name)
        image = pygame.image.load(img_path).convert_alpha()
        return image

    def _load_scaled_image(self, name, scale):
        image = self._load_image(name)
        return pygame.transform.scale(image, scale)

    def _load_image_with_rect(self, name):
        image = self._load_image(name)
        return image, image.get_rect()

    def _load_sound(self, name):
        sound_path = os.path.join(self.snd_dir, name)
        sound = pygame.mixer.Sound(sound_path)
        return sound

    def _load_music(self, name):
        music_path = os.path.join(self.snd_dir, name)
        music = pygame.mixer.music.load(music_path)
        return music

    def load_resources(self):
        self.images['bg'] = self._load_image('black.png')
        self.images['player'] = self._load_image('playerShip1_orange.png')
        mob_img_names = ['meteorBrown_big1.png', 'meteorBrown_med1.png',
                         'meteorGrey_big3.png', 'meteorGrey_med2.png']
        self.images['mob'] = [self._load_image(name) for name in mob_img_names]
        self.images['bullet'] = self._load_image('laserRed07.png')
        self.images['explosion'] = [self._load_image(os.path.join('regularExplosions', f'regularExplosion0{i}.png')) for
                                    i in range(9)]
        self.images['player_explosion'] = [self._load_image(os.path.join('sonicExplosions', f'sonicExplosion0{i}.png'))
                                           for i in range(9)]

        self.images['bonus_shield'] = self._load_image('shield_gold.png')
        self.images['bonus_bolt_big'] = self._load_image('bolt_gold.png')
        self.images['bonus_bolt_small'] = self._load_scaled_image('bolt_gold.png', (20, 20))
        self.images['bonuses'] = [self.images['bonus_bolt_big'], self.images['bonus_shield']]

        self.sounds['music'] = self._load_music('tgfcoder-FrozenJam-SeamlessLoop.mp3')
        mob_snd_names = ['expl3.wav', 'expl6.wav']
        self.sounds['explosion'] = [self._load_sound(name) for name in mob_snd_names]
        self.sounds['pew'] = self._load_sound('pew.wav')



rc = Resources()
