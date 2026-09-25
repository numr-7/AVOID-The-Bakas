import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

# Create a player Rect: (x, y, width, height)
player_rect = pygame.Rect(50, 180, 50, 50)
player_speed = 3
score = 0

running = True
while running:
    # 1. Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check if the click coordinates hit the player's CURRENT bounding box
                if player_rect.collidepoint(event.pos):
                    score += 1
                    print(f"Hit! Score: {score}")

    # 2. Update Game Logic (Move the player continuously)
    player_rect.x += player_speed

    # Bounce off screen edges
    if player_rect.right >= 600 or player_rect.left <= 0:
        player_speed *= -1

    # 3. Draw
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (0, 200, 100), player_rect)  # Green player
    pygame.display.flip()

    clock.tick(60)

pygame.quit()