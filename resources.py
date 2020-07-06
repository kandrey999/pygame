import os
import pygame

dir_name = os.path.dirname(__file__)
img_dir = os.path.join(dir_name, 'arts')
snd_dir = os.path.join(dir_name, 'sounds')


def get_image(name):
    img_path = os.path.join(img_dir, name)
    image = pygame.image.load(img_path).convert_alpha()
    return image


def get_scaled_image(name, scale):
    image = get_image(name)
    return pygame.transform.scale(image, scale)


def get_image_with_rect(name):
    image = get_image(name)
    return image, image.get_rect()


def get_sound(name):
    sound_path = os.path.join(snd_dir, name)
    sound = pygame.mixer.Sound(sound_path)
    return sound


pygame.mixer.music.load(os.path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.mp3'))
pygame.mixer.music.play(loops=-1)
