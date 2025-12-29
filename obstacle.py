import pygame
import random
import math

class Obstacle:
    def __init__(self, x, y, width, height, speed, color, shape_type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.shape_type = shape_type      # Can be jumpable or not jumpable
        self.margin = 5                   # Margin for collision detection

    def move(self):
        self.y += self.speed
    
    def draw(self, window):
        if self.shape_type == "rectangle":
            pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        elif self.shape_type == "circle":
            pygame.draw.circle(window, self.color, (self.x + self.width // 2, self.y + self.height // 2), self.width // 2)
            
    def check_collision(self, player):
        player_rect = player.get_rect()

        if self.shape_type == "rectangle":
            obstacle_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            return player_rect.colliderect(obstacle_rect)
        
        elif self.shape_type == "circle":
            circle_centre_x = self.x + self.width // 2
            circle_centre_y = self.y + self.height // 2
            circle_radius = self.width // 2
            
            closest_x = max(player_rect.left, min(circle_centre_x, player.x + player.width))
            closest_y = max(player_rect.top, min(circle_centre_y, player.y + player.height))

            dx = circle_centre_x - closest_x
            dy = circle_centre_y - closest_y
            distance_sq = math.sqrt(dx ** 2 + dy ** 2)
            
            player_bottom = player.y + player.height
            circle_top = self.y
            if player_bottom <= circle_top:
                return distance_sq < (circle_radius + self.margin)
            
            return False
    
    def reset(self, screen_width, start_y):
        self.y = start_y
        self.shape_type = random.choice(["rectangle", "circle"])


    @classmethod
    def create_row(cls, num_obstacles, screen_width, start_y, speed, color):
        obstacles = []
        gap = screen_width / (num_obstacles - 1)
        # choose a global shift allowance S so the row can move left/right while
        # keeping exact spacing; clamp S so positions stay on-screen
        S = max(0, int(gap / 2.2) - 25 // 2)
        S = min(S, (screen_width - 50) // 4)

        available_span = screen_width - 40 - 2 * S
        if available_span < 0:
            available_span = max(0, screen_width - 40)
            S = 0

        step = available_span / (num_obstacles - 1)
        base_positions = [int(round(S + step * i)) for i in range(num_obstacles)]
        shift = random.randint(-S, S) if S > 0 else 0
        positions = [max(0, min(p + shift, screen_width - 40)) for p in base_positions]

        for x in positions:
            shape_type = random.choice(["rectangle", "circle"])
            obstacles.append(cls(x, start_y, 50, 50, speed, color, shape_type))
        return obstacles
    

class ObstacleManager:
    def __init__(self, spawn_delay):
        self.obstacles = []
        self.spawn_timer = 0
        self.spawn_delay = spawn_delay

    def update(self, player, game_Width, game_Height, obstacle_speed, Obstacle_Color):
        collision = False
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            new_row = Obstacle.create_row(
                num_obstacles=6,
                screen_width=game_Width,
                start_y=-60,
                speed=obstacle_speed,
                color=Obstacle_Color)
            self.obstacles.extend(new_row)
            self.spawn_timer = 0

        for obstacle in self.obstacles[:]:
            obstacle.move()

            if obstacle.check_collision(player):
                collision = True
            if obstacle.y > game_Height + 60:
                self.obstacles.remove(obstacle)

        return collision
