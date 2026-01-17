import pygame  # Importing pygame library to help me code my game.
import random  # Importing random library for random number generation.

class Coin:  # Coin class to manage coin attributes and behavior
    def __init__(self, x, y, size, speed, color=(255, 215, 0)):  # Initialising coin attributes
        self.x = x                # Coin x position
        self.y = y                # Coin y position
        self.size = size          # Coin size
        self.speed = speed        # Coin falling speed
        self.color = color        # Coin color (default gold)
        self.collected = False    # Whether the coin has been collected

    def move(self):               # Function to move coin downwards
        self.y += self.speed      

    def draw(self, window):       # Function to draw the coin on the window
        if not self.collected:
            pygame.draw.circle(window, self.color, (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)

    def check_collision(self, player):  # Function to check if coin collides with player
        if self.collected:
            return False
        player_rect = player.get_rect()
        coin_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        return player_rect.colliderect(coin_rect)

class CoinManager:  # CoinManager class to manage multiple coins
    def __init__(self, spawn_delay):  # Initialising coin manager attributes
        self.coins = []            # List of coins
        self.spawn_timer = 0       # Timer for spawning coins
        self.spawn_delay = spawn_delay  # Delay between coin spawns

    def update(self, player, game_Width, game_Height, coin_speed, coin_counter):  # Updates coins and handles spawning/collision
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