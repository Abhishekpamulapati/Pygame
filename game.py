## Importing python libraries

import pygame
import random
import sys
import os

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = ENEMY_SIZE = 50
BACKGROUND_COLOR = (0, 0, 0)
FPS = 30

# Helper to load animation frames
def load_animation_frames(folder, size):
    frames = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith('.png'):
            img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
            img = pygame.transform.scale(img, (size, size))
            frames.append(img)
    return frames

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames, pos, speed=0):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.animation_timer = 0

    def update(self):
        # Animation logic
        self.animation_timer += 1
        if self.animation_timer >= FPS // 8:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.animation_timer = 0

class Player(AnimatedSprite):
    def __init__(self, frames):
        pos = (WIDTH // 2, HEIGHT - 2 * PLAYER_SIZE)
        super().__init__(frames, pos)
    
    def move(self, dx):
        self.rect.x = max(0, min(WIDTH - PLAYER_SIZE, self.rect.x + dx))

class Enemy(AnimatedSprite):
    def __init__(self, frames, x):
        pos = (x, 0)
        super().__init__(frames, pos)
    
    def update(self):
        super().update()
        self.rect.y += self.speed

def set_level(score):
    if score < 20:
        return 5
    elif score < 40:
        return 8
    elif score < 60:
        return 12
    return 15

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Alien Dodge")
    clock = pygame.time.Clock()
    #font = pygame.font.SysFont("monospace", 35)
    font = pygame.font.SysFont("monospace", 28)

    # Load frames
    player_frames = load_animation_frames('player_aliens', PLAYER_SIZE)
    enemy_frames = load_animation_frames('enemy_aliens', ENEMY_SIZE)

    player = Player(player_frames)
    player_group = pygame.sprite.Group(player)
    enemies = pygame.sprite.Group()

    score = 0
    speed = 5
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-PLAYER_SIZE)
                elif event.key == pygame.K_RIGHT:
                    player.move(PLAYER_SIZE)

        # Spawn enemies
        if len(enemies) < 10 and random.random() < 0.1:
            x = random.randint(0, WIDTH - ENEMY_SIZE)
            enemy = Enemy(enemy_frames, x)
            enemy.speed = speed
            enemies.add(enemy)

        # Update positions
        player_group.update()
        enemies.update()

        # Remove off-screen enemies
        for enemy in list(enemies):
            if enemy.rect.top > HEIGHT:
                enemies.remove(enemy)
                score += 1

        speed = set_level(score)
        for enemy in enemies:
            enemy.speed = speed

        # Check collisions
        if pygame.sprite.spritecollideany(player, enemies):
            game_over = True

        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        player_group.draw(screen)
        enemies.draw(screen)
        label = font.render(f"Score: {score}", True, (255, 255, 0))
        screen.blit(label, (WIDTH - label.get_width() - 20, HEIGHT - label.get_height() - 10))
       # screen.blit(label, (WIDTH - 180, HEIGHT - 50))  # Score fully visible
        pygame.display.update()
        clock.tick(FPS)

    # Game over screen
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    screen.fill(BACKGROUND_COLOR)
    screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, HEIGHT // 2 - 40))
    screen.blit(final_score_text, ((WIDTH - final_score_text.get_width()) // 2, HEIGHT // 2 + 10))
    pygame.display.update()
    pygame.time.delay(3000)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()