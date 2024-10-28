import pygame
import random
import time


pygame.init()


COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255)
}
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Adventure")


FPS = 60
clock = pygame.time.Clock()


player_image = pygame.image.load('player.png')
player_image = pygame.transform.scale(player_image, (50, 50))

asteroid_image = pygame.image.load('asteroid.png')
asteroid_image = pygame.transform.scale(asteroid_image, (50, 50))

bonus_image = pygame.image.load('bonus.png')
bonus_image = pygame.transform.scale(bonus_image, (30, 30))


game_data = {
    'score': 0,
    'lives': 3,
    'asteroid_speed': 3,
    'player_speed': 5,
    'max_asteroid_speed': 10,
    'max_player_speed': 8
}


collected_bonuses = set()


def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, COLORS['white'])
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.invincible = False
        self.invincibility_start_time = 0

    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -game_data['player_speed']
        if keys[pygame.K_RIGHT]:
            self.speedx = game_data['player_speed']
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


        if self.invincible and time.time() - self.invincibility_start_time > 2.5:
            self.invincible = False

    def reset_position(self):
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10

    def activate_invincibility(self):
        self.invincible = True
        self.invincibility_start_time = time.time()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = asteroid_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = game_data['asteroid_speed']

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = game_data['asteroid_speed']


class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bonus_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(3, 5)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(3, 5)


def main():
    running = True


    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    bonuses = pygame.sprite.Group()


    asteroid_list = []
    bonus_list = []

    player = Player()
    all_sprites.add(player)

    for _ in range(8):
        asteroid = Asteroid()
        all_sprites.add(asteroid)
        asteroids.add(asteroid)
        asteroid_list.append(asteroid)

    for _ in range(3):
        bonus = Bonus()
        all_sprites.add(bonus)
        bonuses.add(bonus)
        bonus_list.append(bonus)


    while running:
        clock.tick(FPS)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        if game_data['score'] >= 100:
            if game_data['score'] % 10 == 0:
                game_data['asteroid_speed'] += 0.05
                game_data['player_speed'] += 0.05


            if game_data['asteroid_speed'] > game_data['max_asteroid_speed']:
                game_data['asteroid_speed'] = game_data['max_asteroid_speed']


            if game_data['player_speed'] > game_data['max_player_speed']:
                game_data['player_speed'] = game_data['max_player_speed']


        for asteroid in asteroid_list:
            asteroid.speedy = game_data['asteroid_speed']


        all_sprites.update()


        hits = pygame.sprite.spritecollide(player, asteroids, False)
        if hits and not player.invincible:
            game_data['lives'] -= 1
            player.reset_position()
            player.activate_invincibility()
            if game_data['lives'] == 0:
                running = False


        bonus_hits = pygame.sprite.spritecollide(player, bonuses, True)
        if bonus_hits:
            game_data['score'] += 10
            collected_bonuses.add('bonus')
            bonus = Bonus()
            all_sprites.add(bonus)
            bonuses.add(bonus)
            bonus_list.append(bonus)

        screen.fill(COLORS['black'])
        all_sprites.draw(screen)
        draw_text(screen, f"Score: {game_data['score']}", 18, WIDTH // 2, 10)
        draw_text(screen, f"Lives: {game_data['lives']}", 18, WIDTH // 2, 30)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
