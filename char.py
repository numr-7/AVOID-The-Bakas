import os
import pygame
import random

def load_assets():
    base = os.path.join(os.path.dirname(__file__), "assets")
    return {
        "player": pygame.image.load(os.path.join(base, "gumi.png")).convert_alpha(),
        "anomaly_one": pygame.image.load(os.path.join(base, "miku.png")).convert_alpha(),
        "anomaly_two": pygame.image.load(os.path.join(base, "neru.png")).convert_alpha(),
        "anomaly_three": pygame.image.load(os.path.join(base, "teto.png")).convert_alpha(),
    }

class player:
    def __init__(self, x, y, width, height, speed, screen_width, screen_height, assets):
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.image = pygame.transform.scale(assets["player"], (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def handle_input(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.width))
        self.rect.y = max(0, min(self.rect.y, self.screen_height - self.height))

        self.x = self.rect.x
        self.y = self.rect.y
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def get_rect(self):
        return self.rect

class anomaly_one:
    def __init__(self, width, height,  screen_width, screen_height, assets):
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.image = pygame.transform.scale(assets["anomaly_one"], (width, height))
        self.rect = self.image.get_rect()

        #lifetime
        self.active = False
        self.spawntime = 0
        self.lifespan = 3000

        #hit
        self.game_over = False
    
    def handle_spawn(self):
        random_x = random.randint(0, self.screen_width - self.width)
        random_y = random.randint(0, self.screen_height - self.height)

        self.rect.topleft = (random_x, random_y)
        self.spawntime = pygame.time.get_ticks()
        self.active = True
        print("Miku Spawned!!")

    def handle_despawn(self):
        self.active = False

    def handle_update(self):
        if not self.active:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.spawntime >= self.lifespan:
            print("You lost!")
            self.handle_despawn()
            self.game_over = True

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)

class anomaly_two:
    def __init__(self, width, height, screen_width, screen_height, assets):
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.image = pygame.transform.scale(assets["anomaly_two"], (width, height))
        self.rect = self.image.get_rect()

        #lifetime
        self.active = False
        self.spawntime = 0
        self.lifespan = 5000

        #attack
        self.game_over = False
        self.attack_start = None
        self.attack_end = None

        #attack warning
        self.warning_active = False
        self.attack_active = False

        self.warning_start_time = 0
        self.warning_duration = 1500      # warning lasts longer
        self.attack_start_time = 0
        self.attack_duration = 700        # actual attack is shorter

    def handle_spawn(self):
        random_x = random.randint(0, self.screen_width - self.width)
        random_y = random.randint(0, self.screen_height - self.height)

        self.rect.topleft = (random_x, random_y)
        self.spawntime = pygame.time.get_ticks()
        self.active = True

        self.attack_start = self.rect.center
        random_dest_x = random.randint(0, self.screen_width)
        random_dest_y = random.randint(0, self.screen_height)
        self.attack_end = (random_dest_x, random_dest_y)

        self.warning_active = True
        self.attack_active = False
        self.warning_start_time = pygame.time.get_ticks()
        print("Neru warning started!")

    def handle_despawn(self):
        self.active = False
        self.warning_active = False
        self.attack_active = False

    def attack_intersects(self, player_rect):
        if self.attack_start is None or self.attack_end is None:
            return False

        x1, y1 = self.attack_start
        x2, y2 = self.attack_end

        steps = 30
        for i in range(steps + 1):
            t = i / steps
            x = int(x1 + (x2 - x1) * t)
            y = int(y1 + (y2 - y1) * t)

            if player_rect.collidepoint(x, y):
                return True

        return False

    def handle_update(self, player_rect):
        if not self.active:
            return

        current_time = pygame.time.get_ticks()

        if self.warning_active:
            if current_time - self.warning_start_time >= self.warning_duration:
                self.warning_active = False
                self.attack_active = True
                self.attack_start_time = pygame.time.get_ticks()
                print("Neru beam fired!")
            return

        if self.attack_active:
            if self.attack_intersects(player_rect):
                print("Player Hit!")
                self.game_over = True
                self.attack_active = False
                self.handle_despawn()
                return

            if current_time - self.attack_start_time >= self.attack_duration:
                self.attack_active = False
                self.handle_despawn()
                print("Neru attack over!")

    def draw(self, screen):
        if self.warning_active and self.attack_start and self.attack_end:
            pygame.draw.line(screen, (80, 80, 80), self.attack_start, self.attack_end, 60)

        if self.attack_active and self.attack_start and self.attack_end:
            pygame.draw.line(screen, (80, 80, 80), self.attack_start, self.attack_end, 60)
            pygame.draw.line(screen, (107, 13, 6), self.attack_start, self.attack_end, 50)

        if self.active:
            screen.blit(self.image, self.rect)

class anomaly_three():
    def __init__(self, width, height, screen_width, screen_height, assets):
        