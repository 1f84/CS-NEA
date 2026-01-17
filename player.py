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
        self.is_skin_equipped = False  # Whether the skin is equipped

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
        if self.is_skin_equipped:
            # Layer 1: Black outer border
            border_thickness = 2
            pygame.draw.rect(window, (0, 0, 0), (self.x, self.y, self.width, self.height))
            
            # Layer 2: Cyan layer inside the border
            cyan_layer_size = self.width - border_thickness * 2
            cyan_layer_x = self.x + border_thickness
            cyan_layer_y = self.y + border_thickness
            pygame.draw.rect(window, (34, 240, 255), (cyan_layer_x, cyan_layer_y, cyan_layer_size, cyan_layer_size))
            
            # Layer 3: Thick black inner border to create depth
            inner_border_thickness = 6
            black_inner_size = cyan_layer_size - inner_border_thickness * 2
            black_inner_x = cyan_layer_x + inner_border_thickness
            black_inner_y = cyan_layer_y + inner_border_thickness
            pygame.draw.rect(window, (0, 0, 0), (black_inner_x, black_inner_y, black_inner_size, black_inner_size))
            
            # Layer 4: Cyan core in the center for the final effect
            core_size = black_inner_size - inner_border_thickness * 2
            core_x = black_inner_x + inner_border_thickness
            core_y = black_inner_y + inner_border_thickness
            pygame.draw.rect(window, (34, 240, 255), (core_x, core_y, core_size, core_size))
        else:
            pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def get_rect(self):         # Returns the player's rectangle for collision detection
        return pygame.Rect(self.x, self.y, self.width, self.height)
