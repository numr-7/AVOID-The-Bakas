import pygame
import char
import random

pygame.init()

WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AVOID them!")
clock = pygame.time.Clock()

assets = char.load_assets()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#player variable
player_width = 40
player_height = 40
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

#anomaly spawn event
A1_SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(A1_SPAWN_EVENT, 3000)

A2_SPAWN_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(A2_SPAWN_EVENT, 5000)

A3_SPAWN_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(A3_SPAWN_EVENT, 5000)

running = True
while running:
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

    if miku.game_over:
        print("Game Over!")
        running = False

    if neru.game_over:
        print("Game over!")
        running = False
    
    if teto.game_over:
        print("Game over!")
        running = False

    screen.fill(BLACK)
    player.draw(screen)
    miku.draw(screen)
    neru.draw(screen)
    teto.draw(screen)
    pygame.display.update()

    clock.tick(60)
pygame.quit()