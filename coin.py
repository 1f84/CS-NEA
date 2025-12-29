import pygame
import random

class Coin:
    def __init__(self, x, y, size, speed, color=(255, 215, 0)):  # Gold color
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.collected = False

    def move(self):
        self.y += self.speed

    def draw(self, window):
        if not self.collected:
            pygame.draw.circle(window, self.color, (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)

    def check_collision(self, player):
        if self.collected:
            return False
        player_rect = player.get_rect()
        coin_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        return player_rect.colliderect(coin_rect)

class CoinManager:
    def __init__(self, spawn_delay):
        self.coins = []
        self.spawn_timer = 0
        self.spawn_delay = spawn_delay  # In frames, 10 seconds * 60 FPS = 600

    def update(self, player, game_Width, game_Height, coin_speed, coin_counter):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            # Spawn coin at random x position
            x = random.randint(0, game_Width - 50)
            new_coin = Coin(x, -50, 30, coin_speed)
            self.coins.append(new_coin)
            self.spawn_timer = 0

        for coin in self.coins[:]:
            coin.move()

            if coin.check_collision(player):
                coin.collected = True
                coin_counter[0] += 1  # Increment counter
                self.coins.remove(coin)
            elif coin.y > game_Height + 50:
                self.coins.remove(coin)