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
        "miku_spawn_sfx": [
            # pygame.mixer.Sound(os.path.join(base, "jet2-miku.mp3")),
            pygame.mixer.Sound(os.path.join(base, "mikudayo.mp3"))
        ],
        "neru_spawn_sfx": [
            pygame.mixer.Sound(os.path.join(base, "neru_phone.mp3"))
        ],
        "teto_spawn_sfx": [
            pygame.mixer.Sound(os.path.join(base, "kasane-teto.mp3")),
            pygame.mixer.Sound(os.path.join(base, "teetoo.mp3")),
            pygame.mixer.Sound(os.path.join(base, "teto-wav.mp3"))
        ],
        "collectible": [
            pygame.image.load(os.path.join(base, "bakso.png")),
            pygame.image.load(os.path.join(base, "mieayam.png")),
            pygame.image.load(os.path.join(base, "sateayam.png")),
            pygame.image.load(os.path.join(base, "nasi_ayam_bakar.png"))
        ]
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

class collectible:
    def __init__(self, width, height, screen_width, screen_height, assets):
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.item_choices = assets["collectible"]

        self.image = None
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.active = False

    def handle_spawn(self):
        self.image = pygame.transform.scale(random.choice(self.item_choices), (self.width, self.height))
        self.rect.size = self.image.get_size()
        self.rect.x = random.randint(20, self.screen_width - 50)
        self.rect.y = random.randint(20, self.screen_height - 50)
        self.active = True

    def handle_update(self, player_rect):
        if not self.active:
            return False

        if self.rect.colliderect(player_rect):
            self.active = False
            return True

        return False

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)

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

        self.spawn_sfx = assets["miku_spawn_sfx"]
    
    def handle_spawn(self):
        random_x = random.randint(0, self.screen_width - self.width)
        random_y = random.randint(0, self.screen_height - self.height)

        self.rect.topleft = (random_x, random_y)
        self.spawntime = pygame.time.get_ticks()
        self.active = True

        sfx = random.choice(self.spawn_sfx)
        sfx.play()
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

        self.spawn_sfx = assets["neru_spawn_sfx"]

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
        sfx = random.choice(self.spawn_sfx)
        sfx.play()

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
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.image = pygame.transform.scale(assets["anomaly_three"], (width, height))
        self.rect = self.image.get_rect()

        self.active = False
        self.game_over = False

        self.spawn_sfx = assets["teto_spawn_sfx"]

        self.state = "idle"
        self.warning_dur = 3000
        self.fall_dur = 1000

        self.spawn_time = 0
        self.fall_start_time = 0

        self.indicator_pos = None
        self.start_pos = None
        self.target_pos = None

    def handle_spawn(self):
        self.active = True
        self.game_over = False
        self.state = "warning"
        self.spawn_time = pygame.time.get_ticks()
        self.fall_start_time = 0


        #spawn above screen
        self.start_pos = (self.screen_width // 2 - self.width // 2, -self.height)
        self.rect.topleft = self.start_pos

        #random target zone
        margin = 80
        target_x = random.randint(margin, self.screen_width - margin - self.width)
        target_y = random.randint(self.height + 60, self.screen_height - self.height - 60)

        self.target_pos = (target_x, target_y)
        self.indicator_pos = self.target_pos

        print("Fatass spawned!")

    def handle_update(self, player_rect):
        if not self.active:
            return

        now = pygame.time.get_ticks()

        if self.state == "warning":
            if now - self.spawn_time >= self.warning_dur:
                self.state = "falling"
                self.fall_start_time = now
                sfx = random.choice(self.spawn_sfx)
                sfx.play()
            return
        
        if self.state == "falling":
            elapsed = now - self.fall_start_time
            progress = min(elapsed / self.fall_dur, 1.0)
        
            start_x, start_y = self.start_pos
            target_x, target_y = self.target_pos

            x = int(start_x + (target_x - start_x) * progress)
            y = int(start_y + (target_y - start_y) * progress)

            self.rect.center = (x, y)

            if progress >= 1.0:
                self.state = "landed"
                self.game_over = self.rect.colliderect(player_rect)
                self.handle_despawn()
            return
    
    def handle_despawn(self):
        self.active = False
        self.state = "idle"
        self.indicator_pos = None
        self.start_pos = None
        self.target_pos = None
        self.fall_start_time = 0
    
    def draw(self, screen):
        if not self.active:
            return
        
        if self.state == "warning" and self.indicator_pos:
            x, y = self.indicator_pos
            pygame.draw.ellipse(screen, (120, 120, 120), (x - 50, y - 30, 100, 60), 3)
            pygame.draw.circle(screen, (220, 220, 220), (x, y), 9)
        
        if self.state in ("falling", "landed"):
            x, y = self.indicator_pos
            pygame.draw.ellipse(screen, (120, 120, 120), (x - 50, y - 30, 100, 60), 3)
            pygame.draw.circle(screen, (220, 220, 220), (x, y), 9)
            screen.blit(self.image, self.rect)