import pygame
import char
import random

pygame.init()

WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AVOID The Bakas!")
clock = pygame.time.Clock()

assets = char.load_assets()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#player variable
player_width = 60
player_height = 60
player_speed = 5
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT // 2 - player_height // 2

#anomaly variable
anomaly_width = 150
anomaly_height = 150

#char defines
player = char.player(player_x, player_y, player_width, player_height, player_speed, WIDTH, HEIGHT, assets)
miku = char.anomaly_one(anomaly_width, anomaly_height, WIDTH, HEIGHT, assets)
neru = char.anomaly_two(anomaly_width, anomaly_height, WIDTH, HEIGHT, assets)
teto = char.anomaly_three(anomaly_width, anomaly_height, WIDTH, HEIGHT, assets)
item = char.collectible(player_width, player_height, WIDTH, HEIGHT, assets)

#anomaly spawn event
A1_SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(A1_SPAWN_EVENT, 3000)

A2_SPAWN_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(A2_SPAWN_EVENT, 5000)

A3_SPAWN_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(A3_SPAWN_EVENT, 5000)

ITEM_SPAWN_EVENT = pygame.USEREVENT + 4
pygame.time.set_timer(ITEM_SPAWN_EVENT, 1500)

score = 0
hit = False
game_over_time = 0
game_over_delay = 3000
final_elapsed_time = 0.0
final_score = 0

running = True
while running:
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print("Game quitted!")

        if event.type == A1_SPAWN_EVENT:
            if not miku.active:
                miku.handle_spawn()

        if event.type == A2_SPAWN_EVENT:
            if not neru.active:
                neru.handle_spawn()

        if event.type == A3_SPAWN_EVENT:
            if not teto.active:
                teto.handle_spawn()

        if event.type == ITEM_SPAWN_EVENT:
            if not item.active:
                item.handle_spawn()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if miku.active and event.button == 1:
                if miku.rect.collidepoint(event.pos):
                    miku.handle_despawn()
                    print("Miku avoided!")
    
    keys = pygame.key.get_pressed()
    player_rect = player.get_rect()

    #object updates
    player.handle_input(keys)
    miku.handle_update()
    neru.handle_update(player_rect)
    teto.handle_update(player_rect)

    if item.active:
        if item.handle_update(player_rect):
            score += 1
            print("Score +1")

    if miku.game_over or neru.game_over or teto.game_over:
        if not hit:
            hit = True
            game_over_time = now
            final_elapsed_time = now /1000.0
            final_score = (final_elapsed_time / 20) + score
            print("Player got hit!")
    
    elapsed_seconds = final_elapsed_time if hit else now / 1000.0

    if hit and now - game_over_time >= game_over_delay:
        running = False

    screen.fill(BLACK)
    player.draw(screen)
    miku.draw(screen)
    neru.draw(screen)
    teto.draw(screen)
    item.draw(screen)

    elapsed_text = f"Time: {elapsed_seconds:.1f}s"
    score_text = f"Score: {score}"
    font = pygame.font.SysFont(None, 30)

    screen.blit(font.render(elapsed_text, True, WHITE), (10, 10))
    screen.blit(font.render(score_text, True, WHITE), (10, 40))

    if hit:
        screen.blit(font.render(f"Final Score: {final_score:.2f}", True, WHITE), (WIDTH // 2 - 120, HEIGHT // 2))

    pygame.display.update()

    clock.tick(60)
pygame.quit()