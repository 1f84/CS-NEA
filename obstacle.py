import pygame  # Importing pygame library to help me code my game.
import random  # Importing random library for random number generation.
import math    # Importing math library for mathematical calculations.

# Represents game obstacles
class Obstacle:  # Obstacle class to manage individual obstacles
    # Initialize obstacle properties
    def __init__(self, x, y, width, height, speed, color, shape_type):  # Initialising obstacle attributes
        self.x = x                # Obstacle x position
        self.y = y                # Obstacle y position
        self.width = width        # Obstacle width
        self.height = height      # Obstacle height
        self.speed = speed        # Obstacle falling speed
        self.color = color        # Obstacle color
        self.shape_type = shape_type      # Obstacle shape type (rectangle or circle)
        self.margin = 5                  # Collision margin
    # Move obstacle downwards
    def move(self):  # Function to move obstacle downwards
        self.y += self.speed
    
    # Draw obstacle on screen
    def draw(self, window):  # Function to draw the obstacle on the window
        if self.shape_type == "rectangle":
            pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        elif self.shape_type == "circle":
            pygame.draw.circle(window, self.color, (self.x + self.width // 2, self.y + self.height // 2), self.width // 2)
            
    # Check for collision with player
    def check_collision(self, player):  # Function to check if obstacle collides with player
        player_rect = player.get_rect()

        if self.shape_type == "rectangle":               # Collision detection for rectangle obstacle
            obstacle_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            return player_rect.colliderect(obstacle_rect)
        
        elif self.shape_type == "circle":                # Collision detection for circle obstacle
            circle_centre_x = self.x + self.width // 2  # Calculate circle center x
            circle_centre_y = self.y + self.height // 2  # Calculate circle center y
            circle_radius = self.width // 2              # Circle radius
            
            # Find the closest point on the player rect to the circle center
            closest_x = max(player_rect.left, min(circle_centre_x, player.x + player.width))
            closest_y = max(player_rect.top, min(circle_centre_y, player.y + player.height))

            # Calculate distance from circle center to closest point
            dx = circle_centre_x - closest_x
            dy = circle_centre_y - closest_y
            distance_sq = math.sqrt(dx ** 2 + dy ** 2)
            
            # Special case: if player is above the circle, check bottom collision
            player_bottom = player.y + player.height
            circle_top = self.y
            if player_bottom <= circle_top:
                return distance_sq < (circle_radius + self.margin)
            
            return False
    
    # Reset obstacle position and shape
    def reset(self, screen_width, start_y):  # Function to reset obstacle position and shape
        self.y = start_y
        self.shape_type = random.choice(["rectangle", "circle"])


    # Create a row of obstacles
    @classmethod
    def create_row(cls, num_obstacles, screen_width, start_y, speed, color):  # Class method to create a row of obstacles
        obstacles = []
        gap = screen_width / (num_obstacles - 1)  # Calculate gap between obstacles
        # Choose a global shift allowance S so the row can move left/right while keeping exact spacing
        # Clamp S so positions stay on-screen
        S = max(0, int(gap / 2.2) - 25 // 2)
        S = min(S, (screen_width - 50) // 4)

        # Calculate available span for positioning, accounting for margins
        available_span = screen_width - 40 - 2 * S
        if available_span < 0:
            available_span = max(0, screen_width - 40)
            S = 0

        # Calculate step size for even spacing
        step = available_span / (num_obstacles - 1)
        # Generate base positions
        base_positions = [int(round(S + step * i)) for i in range(num_obstacles)]
        # Apply random shift to vary row position
        shift = random.randint(-S, S) if S > 0 else 0
        # Ensure positions are within screen bounds
        positions = [max(0, min(p + shift, screen_width - 40)) for p in base_positions]

        # Create obstacles at calculated positions
        for x in positions:
            shape_type = random.choice(["rectangle", "circle"])
            obstacles.append(cls(x, start_y, 50, 50, speed, color, shape_type))
        return obstacles
    

# Manages obstacle spawning and updates
class ObstacleManager:  # ObstacleManager class to manage multiple obstacles
    # Initialize obstacle manager
    def __init__(self, spawn_delay):  # Initialising obstacle manager attributes
        self.obstacles = []        # List of obstacles
        self.spawn_timer = 0       # Timer for spawning obstacles
        self.spawn_delay = spawn_delay  # Delay between obstacle spawns

    # Update obstacles: spawn, move, check collisions
    def update(self, player, game_Width, game_Height, obstacle_speed, Obstacle_Color):  # Updates obstacles and checks for collisions
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
