import pygame
import random
import sys

# Константы
WIDTH, HEIGHT = 600, 400
PLAYER_SIZE = 20
ENEMY_SIZE = 20
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Класс Игрока
class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)
        self.direction = (0, 0)  # Движение начнется после выбора направления

    def move(self):
        # Обновление позиции игрока
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]

        # Ограничение игрока в пределах окна
        self.rect.x = max(0, min(WIDTH - PLAYER_SIZE, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - PLAYER_SIZE, self.rect.y))

    def change_direction(self, direction):
        self.direction = direction

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect)

# Класс Врага
class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - ENEMY_SIZE),
                                random.randint(0, HEIGHT - ENEMY_SIZE),
                                ENEMY_SIZE, ENEMY_SIZE)
        self.speed = random.randint(2, 5)
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def move(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # Отражение от границ окна
        if self.rect.x <= 0 or self.rect.x >= WIDTH - ENEMY_SIZE:
            self.direction = (-self.direction[0], self.direction[1])
        if self.rect.y <= 0 or self.rect.y >= HEIGHT - ENEMY_SIZE:
            self.direction = (self.direction[0], -self.direction[1])

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

# Класс Игры
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Игра на выживание")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.player = Player()
        self.enemies = []
        self.spawn_timer = 0
        self.score = 0
        self.running = True
        self.game_over = False

    def reset_game(self):
        self.player = Player()
        self.enemies = []
        self.spawn_timer = 0
        self.score = 0
        self.game_over = False

    def spawn_enemy(self):
        if self.spawn_timer <= 0:
            self.enemies.append(Enemy())
            self.spawn_timer = 60  # Пауза между появлениями врагов
        else:
            self.spawn_timer -= 1

    def check_collision(self):
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.game_over = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()

        keys = pygame.key.get_pressed()
        if not self.game_over:
            if keys[pygame.K_UP]:
                self.player.change_direction((0, -5))
            elif keys[pygame.K_DOWN]:
                self.player.change_direction((0, 5))
            elif keys[pygame.K_LEFT]:
                self.player.change_direction((-5, 0))
            elif keys[pygame.K_RIGHT]:
                self.player.change_direction((5, 0))

    def update(self):
        if not self.game_over:
            self.player.move()
            for enemy in self.enemies:
                enemy.move()
            self.spawn_enemy()
            self.check_collision()
            self.score += 1

    def draw(self):
        self.screen.fill(BLACK)
        if not self.game_over:
            self.player.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            self.draw_text(f"Счет: {self.score}", WIDTH // 2, 20)
        else:
            self.draw_text("GAME OVER", WIDTH // 2, HEIGHT // 2 - 20)
            self.draw_text("Нажмите ПРОБЕЛ для рестарта", WIDTH // 2, HEIGHT // 2 + 20)
            self.draw_text(f"Ваш счет: {self.score}", WIDTH // 2, HEIGHT // 2 + 60)
        pygame.display.flip()

    def draw_text(self, text, x, y):
        text_obj = self.font.render(text, True, WHITE)
        text_rect = text_obj.get_rect(center=(x, y))
        self.screen.blit(text_obj, text_rect)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()
