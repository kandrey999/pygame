import os
import pygame
from pygame.sprite import Group

from player import Player
from entities import *
from resources import rc
from os import path


class App:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self._size = self._width, self._height = 800, 600
        self._screen = pygame.display.set_mode(self._size)
        rc.load_resources()
        self._bg = pygame.transform.scale(rc.images['bg'], self._size)
        self._key_states = pygame.key.get_pressed()
        self._clock = pygame.time.Clock()
        self._running = True
        self._game_over = True
        self._restart = True
        pygame.mixer.music.play(loops=-1)

        self._all_sprites = Group()
        self._bonuses = Group()
        self._bullets = Group()
        self._mobs = Group()

        self._player = Player((self._width / 2, self._height - 10), self._all_sprites, self._bullets)
        self._all_sprites.add(self._player)

        self._mob_count = 0
        for i in range(self._mob_count):
            self.create_mob()
        # progress_bar = ProgressBar(10, 10, value=100, height=15)
        # all_sprites.add(progress_bar)
        self._player_health_bar = PlayerHealthProgressBar(self._player)
        self._all_sprites.add(self._player_health_bar)

        self._scoreBar = TextLabel((self._width / 2, 10))
        self._all_sprites.add(self._scoreBar)

        self._player_lives_bar = PlayerLivesProgressBar(self._size[0] - 10, 0, self._player)
        self._all_sprites.add(self._player_lives_bar)

        self._gun_power_progress_bar = GunPowerImageProgressBar(self._size[0] - 10, self._size[1] - 40, self._player)
        self._all_sprites.add(self._gun_power_progress_bar)

    @property
    def restart(self):
        return self._restart

    # @restart.setter
    # def restart(self, value):
    #     print('set restart')
    #     self._restart = value

    # def init_sprites(self):
    #     self._all_sprites = Group()
    #     self._bonuses = Group()
    #     self._bullets = Group()
    #     self._mobs = Group()
    #     self._mob_count = 10
    #     self._player = Player((self._width / 2, self._height - 10), self._all_sprites, self._bullets)
    #     self._all_sprites.add(self._player)
    #
    #     for i in range(self._mob_count):
    #         self.create_mob()
    #
    #     # progress_bar = ProgressBar(10, 10, value=100, height=15)
    #     # all_sprites.add(progress_bar)
    #     self._player_health_bar = PlayerHealthProgressBar(self._player)
    #     self._all_sprites.add(self._player_health_bar)
    #
    #     self._scoreBar = TextLabel((self._width / 2, 10))
    #     self._all_sprites.add(self._scoreBar)
    #
    #     self._player_lives_bar = PlayerLivesProgressBar(self._size[0] - 10, 0, self._player)
    #
    #     self._all_sprites.add(self._player_lives_bar)
    #
    #     self._gun_power_progress_bar = GunPowerImageProgressBar(self._size[0] - 10, self._size[1] - 40, self._player)
    #
    #     self._all_sprites.add(self._gun_power_progress_bar)

    def _event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('quit')
                self._running = False
                self.restart = False
            if event.type in (pygame.KEYUP, pygame.KEYDOWN):
                self._key_states = pygame.key.get_pressed()

    def create_mob(self):
        Mob(self._size,
            self._all_sprites, self._mobs)

    def check_count_mob(self):
        if len(self._mobs) < self._mob_count:
            for i in range(self._mob_count - len(self._mobs)):
                self.create_mob()

    def start_screen(self):
        start_labels = Group()
        t1 = TextLabel((self._width / 2 - 50, 150), 'Star Wars')
        t2 = TextLabel((self._width / 2 - 50, 250), 'arrows to control, space to fire')
        # t3 = TextLabel((self._width / 2 - 50, 350), 'press LSHIFT key to start')
        t4 = TextLabel((self._width / 2 - 50, 350), '1-easy, 2-normal, 3-hard')
        start_labels.add(t1, t2, t4)
        self._screen.blit(self._bg, self._bg.get_rect())
        start_labels.draw(self._screen)
        pygame.display.flip()
        # waiting = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('quit')
                self._running = False
                self.restart = False
            # if event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
            #     self._game_over = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    self._mob_count = 5
                    self._game_over = False
                elif event.key == pygame.K_2:
                    self._mob_count = 15
                    self._game_over = False
                elif event.key == pygame.K_3:
                    self._mob_count = 25
                    self._game_over = False
        # init_and_run_app()
        # self.init_sprites()

    def check_collide_player_with_mobs_and_react(self):
        hits = pygame.sprite.spritecollide(self._player, self._mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            self._player.on_damage(hit.radius)
            if self._player.health <= 0:
                # player_explosion_images = [rc.get_image(path.join('sonicExplosions', f'sonicExplosion0{i}.png')) for i
                #                            in range(9)]
                player_explosion = PlayerExplosion(self._player.rect.center)
                self._all_sprites.add(player_explosion)
                self._player.hide()
                self._player.on_destroy()
            explosion_size = hit.radius * 2
            explosion = Explosion(hit.rect.center, explosion_size)
            self._all_sprites.add(explosion)

    def check_collide_bullets_with_mobs_and_react(self):
        """check collide bullets with mobs and react"""
        hits = pygame.sprite.groupcollide(self._mobs, self._bullets, True, True)
        for hit in hits:
            self._scoreBar.text = int(self._scoreBar.text) + 50 - hit.radius
            # self.create_mob()
            hit.explosion_sound.play()
            explosion_size = hit.radius * 2
            # explosion_images = [rc.get_scaled_image(path.join('regularExplosions', f'regularExplosion0{i}.png'),
            #                                         (explosion_size, explosion_size)) for i in range(9)]
            explosion = Explosion(hit.rect.center, explosion_size)
            self._all_sprites.add(explosion)
            if randint(1, 100) > 95:
                bonus = Bonus(hit.rect.center, self._height)
                self._all_sprites.add(bonus)
                self._bonuses.add(bonus)

    # def check(self):
    #     if self._game_over:
    #         self._game_over = False
    #         self.start_screen()
    #         self.init_sprites()

    def update(self):
        print(self._mob_count)
        self._player.update2(self._key_states, self._size)
        self.check_collide_player_with_mobs_and_react()

        if self._player.hidden and pygame.time.get_ticks() - self._player.hide_time > 1000:
            self._player.show()

        if self._player.lives == 0:
            self._running = False
            # self._restart = False
            # self._player.lives = 1
            # self._game_over = True
            # self._running = False
            # restart_and_run_app()

        # self._game_over = True
        # init_and_run_app()
        # self._game_over = True
        # init_and_run_app()

        self.check_collide_bullets_with_mobs_and_react()

        hits3 = pygame.sprite.spritecollide(self._player, self._bonuses, True)
        for hit in hits3:
            self._player.on_catch_bonus(hit)

        self.check_count_mob()
        self._all_sprites.update()

    def render(self):
        self._screen.blit(self._bg, self._bg.get_rect())

        self._all_sprites.draw(self._screen)
        pygame.display.update()

    def run_app(self):
        while self._running:
            # print(self._running)
            self._clock.tick(30)
            if self._game_over:
                self.start_screen()
                # init_and_run_app()
            else:
                self._event_loop()
                self.update()
                self.render()

# def restart_and_run_app():
#     app = App()
#     app.run_app()
