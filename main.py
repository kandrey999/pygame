import pygame
from constants import *
from game_controller import GameController

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

import resources as rc

space_img, space_img_rect = rc.get_image_with_rect('black.png')
space_img = pygame.transform.scale(space_img, (WIDTH, HEIGHT))

from entities import *

# player_health.draw()
# all_sprites.add(player_health)

controller = GameController(player)

# score = 0


# def print_score():
#     font = pygame.font.Font(pygame.font.match_font('arial'), 20)
#     text = font.render(str(score), True, WHITE)
#     text_rect = text.get_rect(midtop=(WIDTH / 2, 10))
#     screen.blit(text, text_rect)

# def print_health():
#     BAR_LENGTH = 100
#     BAR_HEIGHT = 200


running = True
while running:
    clock.tick(FPS)
    controller.handle_events()

    hits1 = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits1:
        progress_bar.value -= hit.radius
        if progress_bar.value <= 0:
            player_explosion = PlayerExplosion(player.rect.center)
            all_sprites.add(player_explosion)
            player.hide()
            player.lives -= 1
            player_health_bar.value -= 1

            # player_health.draw(player.lives)
            # player.god = True
            progress_bar.value = progress_bar.max_value

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
