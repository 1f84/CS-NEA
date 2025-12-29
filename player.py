import pygame  # Importing pygame library to help me code my game.

class Player:                                        # Player class to manage player, and attributes
    def __init__(self, x, y, width, height, speed):  # Initialising player attributes
        self.x = x                # Player x position
        self.y = y                # Player y position
        self.width = width        # Player width
        self.height = height      # Player height
        self.speed = speed        # Player speed
        self.jumping = False      # Is the player jumping
        self.vel_y = 0            # Vertical velocity
        self.gravity = 0.5        # Gravity effect
        self.ground_y = y         # Ground level
        self.jump_strength = -12  # Jump strength
        self.color = (50, 150, 250)  # Player color

    def move_left(self):          # Function to move player left
        self.x -= self.speed      
        if self.x < 0:
            self.x = 0

    def move_left_tap(self):       # Function to move player left on tap (smaller distance)
        self.x -= 4
        if self.x < 0:
            self.x = 0

    def move_right(self, screen_width):         # Function to move player right
        self.x += self.speed
        if self.x + self.width > screen_width:
            self.x = screen_width - self.width

    def move_right_tap(self, screen_width):     # Function to move player right on tap (smaller distance)
        self.x += 4
        if self.x + self.width > screen_width:
            self.x = screen_width - self.width

    def jump(self):                # Function to make the player jump
        if not self.jumping:
            self.jumping = True
            self.vel_y = self.jump_strength

    def update(self, ground_y):              # Updates the position of the player and handles jumping
        self.y += self.vel_y
        self.vel_y += self.gravity
        
        if self.y + self.height >= ground_y:  # Check if player is on the ground if so, it reset jumping
            self.y = ground_y - self.height
            self.jumping = False
            self.vel_y = 0

    def draw(self, window,):        # Draws the player on the game window
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def get_rect(self):         # Returns the player's rectangle for collision detection
        return pygame.Rect(self.x, self.y, self.width, self.height)
