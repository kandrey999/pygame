import pygame
from constants import *
# from game_controller import GameController
from resources import *
from entities import *
from pygame.sprite import Group
from player import *


# from groups import *


class GameController:
    def __init__(self, player):
        self.player = player

    def handle_events(self):

        player = self.player

        # print(player.speed)



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
        if player.rect.bottom > HEIGHT and not player.hidden:
            player.rect.bottom = HEIGHT


class Game:
    def __init__(self):
        pass

    def run(self):
        all_sprites = Group()
        bonuses = Group()
        bullets = Group()
        mobs = Group()
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("My Game")
        clock = pygame.time.Clock()

        pygame.mixer.music.load(os.path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.mp3'))
        pygame.mixer.music.play(loops=-1)

        space_img, space_img_rect = rc.get_image_with_rect('black.png')
        space_img = pygame.transform.scale(space_img, (WIDTH, HEIGHT))

        player = Player((WIDTH / 2, HEIGHT - 10), all_sprites, bullets)
        controller = GameController(player)
        all_sprites.add(player)
        for i in range(MOB_COUNT):
            mob = Mob(all_sprites, mobs)

        # progress_bar = ProgressBar(10, 10, value=100, height=15)
        # all_sprites.add(progress_bar)
        player_health_bar = PlayerHealthProgressBar(player)
        all_sprites.add(player_health_bar)

        score = TextLabel((WIDTH / 2, 10))
        all_sprites.add(score)

        player_lives_bar = PlayerLivesProgressBar(player)
        all_sprites.add(player_lives_bar)

        gun_power_progress_bar = GunPowerImageProgressBar(player)
        all_sprites.add(gun_power_progress_bar)

        running = True
        while running:
            # print(player.power, player.power_time)
            clock.tick(FPS)
            controller.handle_events()

            hits1 = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
            for hit in hits1:
                player.on_damage(hit.radius)
                if player.health <= 0:
                    player_explosion = PlayerExplosion(player.rect.center)
                    all_sprites.add(player_explosion)
                    player.hide()
                    player.on_destroy()

                explosion = Explosion(hit.rect.center, hit.radius * 2)
                all_sprites.add(explosion)

                mob = Mob(all_sprites, mobs)
            if player.hidden and pygame.time.get_ticks() - player.hide_time > 1000:
                player.show()

            if player.lives == 0 and not player_explosion.alive():
                running = False

            hits2 = pygame.sprite.groupcollide(mobs, bullets, True, True)
            for hit in hits2:
                score.text = int(score.text) + 50 - hit.radius
                mob = Mob(all_sprites, mobs)
                hit.explosion_sound.play()
                explosion = Explosion(hit.rect.center, hit.radius * 2)
                all_sprites.add(explosion)
                bonus = Bonus(hit.rect.center)
                all_sprites.add(bonus)
                bonuses.add(bonus)

            hits3 = pygame.sprite.spritecollide(player, bonuses, True)
            for hit in hits3:
                player.on_catch_bonus(hit)
            # if hits:
            #     print(hits, len(bullets), len(mobs), len(all_sprites))
            # for mob in hits:
            #     mob = Mob()

            all_sprites.update()

            screen.blit(space_img, space_img_rect)
            all_sprites.draw(screen)

            # print_score()
            # screen.blit(Factory.get_space_image(), (800, 600))
            pygame.display.update()


# def init_groups():
#     all_sprites = Group()
#     bonuses = Group()
#     bullets = Group()
#     mobs = Group()
#
#
# def init_pygame():
#     pygame.init()
#     pygame.mixer.init()
#     screen = pygame.display.set_mode(SIZE)
#     pygame.display.set_caption("My Game")
#     clock = pygame.time.Clock()
#
#     pygame.mixer.music.load(os.path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.mp3'))
#     pygame.mixer.music.play(loops=-1)
#
#     space_img, space_img_rect = rc.get_image_with_rect('black.png')
#     space_img = pygame.transform.scale(space_img, (WIDTH, HEIGHT))
#
#
# # player_health.draw()
# # all_sprites.add(player_health)
#
#
# def init_sprites():
#     player = Player((WIDTH / 2, HEIGHT - 10), all_sprites, bullets)
#     all_sprites.add(player)
#     for i in range(MOB_COUNT):
#         mob = Mob(all_sprites, mobs)
#
#     # progress_bar = ProgressBar(10, 10, value=100, height=15)
#     # all_sprites.add(progress_bar)
#     player_health_bar = PlayerHealthProgressBar(player)
#     all_sprites.add(player_health_bar)
#
#     score = TextLabel((WIDTH / 2, 10))
#     all_sprites.add(score)
#
#     player_lives_bar = PlayerLivesProgressBar(player)
#     all_sprites.add(player_lives_bar)
#
#     gun_power_progress_bar = GunPowerImageProgressBar(player)
#     all_sprites.add(gun_power_progress_bar)


# score = 0


# def print_score():
#     font = pygame.font.Font(pygame.font.match_font('arial'), 20)
#     text = font.render(str(score), True, WHITE)
#     text_rect = text.get_rect(midtop=(WIDTH / 2, 10))
#     screen.blit(text, text_rect)

# def print_health():
#     BAR_LENGTH = 100
#     BAR_HEIGHT = 200

# def run():
#     running = True
#     while running:
#         # print(player.power, player.power_time)
#         clock.tick(FPS)
#         controller.handle_events()
#
#         hits1 = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
#         for hit in hits1:
#             player.on_damage(hit.radius)
#             if player.health <= 0:
#                 player_explosion = PlayerExplosion(player.rect.center)
#                 all_sprites.add(player_explosion)
#                 player.hide()
#                 player.on_destroy()
#
#             explosion = Explosion(hit.rect.center, hit.radius * 2)
#             all_sprites.add(explosion)
#
#             mob = Mob(all_sprites, mobs)
#         if player.hidden and pygame.time.get_ticks() - player.hide_time > 1000:
#             player.show()
#
#         if player.lives == 0 and not player_explosion.alive():
#             running = False
#
#         hits2 = pygame.sprite.groupcollide(mobs, bullets, True, True)
#         for hit in hits2:
#             score.text = int(score.text) + 50 - hit.radius
#             mob = Mob(all_sprites, mobs)
#             hit.explosion_sound.play()
#             explosion = Explosion(hit.rect.center, hit.radius * 2)
#             all_sprites.add(explosion)
#             bonus = Bonus(hit.rect.center)
#             all_sprites.add(bonus)
#             bonuses.add(bonus)
#
#         hits3 = pygame.sprite.spritecollide(player, bonuses, True)
#         for hit in hits3:
#             player.on_catch_bonus(hit)
#         # if hits:
#         #     print(hits, len(bullets), len(mobs), len(all_sprites))
#         # for mob in hits:
#         #     mob = Mob()
#
#         all_sprites.update()
#
#         screen.blit(space_img, space_img_rect)
#         all_sprites.draw(screen)
#
#         # print_score()
#         # screen.blit(Factory.get_space_image(), (800, 600))
#         pygame.display.update()
