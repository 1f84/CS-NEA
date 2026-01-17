import time  # Importing time library for timing functions.

def load_high_score():  # Function to load high score from file
    """Load the high score from high_score.txt, return 0 if file doesn't exist"""
    try:
        with open('high_score.txt', 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0

def save_high_score(score):  # Function to save high score to file
    """Save the high score to high_score.txt"""
    with open('high_score.txt', 'w') as f:
        f.write(str(score))

class GameManager:  # GameManager class to manage overall game state and logic
    def __init__(self, player, obstacle_manager, coin_manager, input_manager, shop_manager, pause_manager):  # Initialising game manager with all components
        self.player = player                    # Player object
        self.obstacle_manager = obstacle_manager  # Obstacle manager
        self.coin_manager = coin_manager        # Coin manager
        self.input_manager = input_manager      # Input manager
        self.shop_manager = shop_manager        # Shop manager
        self.pause_manager = pause_manager      # Pause manager
        
        self.game_over = False                  # Whether the game is over
        self.coin_counter = [0]                 # Coin counter (mutable list)
        self.score = 0                          # Current game score
        self.high_score = load_high_score()     # High score loaded from file
        self.game_start_time = 0                # Game start time
        self.last_speed_increase = 0            # Last speed increase time
        self.current_obstacle_speed = 6         # Starting obstacle speed
        self.speed_increase_interval = 15       # Speed increase interval in seconds
    
    def reset_game(self, game_width, ground_y):  # Function to reset game state for new game
        """Reset game state for a new game"""
        self.game_over = False
        self.pause_manager.reset()
        self.player.x, self.player.y = game_width // 2 - 25, ground_y - self.player.height
        self.obstacle_manager.obstacles.clear()
        self.obstacle_manager.spawn_timer = 0
        self.coin_manager.coins.clear()
        self.coin_manager.spawn_timer = 0
        self.coin_counter[0] = 0
        self.score = 0                          # Reset score
        self.input_manager.last_move_time = time.time()
        self.player.vel_y = 0
        self.player.jumping = False
        # Reset speed progression
        self.game_start_time = time.time()
        self.last_speed_increase = 0
        self.current_obstacle_speed = 6
    
    def update_game(self, game_width, game_height, obstacle_color, ground_y):  # Function to update game logic
        """Update game logic (only when not paused)"""
        if self.game_over or self.pause_manager.paused:
            return
        
        # Update speed progression
        current_time = time.time() - self.game_start_time  # Time elapsed since game start
        speed_level = int(current_time // self.speed_increase_interval)  # Calculate current speed level
        if speed_level > self.last_speed_increase:  # If new speed level reached
            self.current_obstacle_speed += 1  # Increase speed by 1 every 15 seconds
            self.last_speed_increase = speed_level  # Update last speed increase level
        
        # Update score based on time survived
        self.score = int(current_time)  # Score is time in seconds
        
        action = self.input_manager.handle(self.player, game_width, self.game_over)
        
        # Check for inactivity timeout
        if time.time() - self.input_manager.last_move_time > 5:
            self.game_over = True
            self.handle_game_over()  # Handle game over logic
            self.shop_manager.add_coins(self.coin_counter[0])
            return
        
        self.player.update(ground_y)
        
        # Check for collisions
        if self.obstacle_manager.update(self.player, game_width, game_height, self.current_obstacle_speed, obstacle_color):
            self.game_over = True
            self.handle_game_over()  # Handle game over logic
            self.shop_manager.add_coins(self.coin_counter[0])
            return
        
        self.coin_manager.update(self.player, game_width, game_height, self.current_obstacle_speed, self.coin_counter)
    
    def draw_game(self, window, text_manager, game_width):  # Function to draw game elements
        """Draw the game elements"""
        if self.pause_manager.paused:
            self.pause_manager.draw_paused_screen(window, self.player, self.obstacle_manager, 
                                                self.coin_manager, self.coin_counter)
        else:
            self.player.draw(window)
            for obstacle in self.obstacle_manager.obstacles:
                obstacle.draw(window)
            for coin in self.coin_manager.coins:
                coin.draw(window)
            
            # Draw UI
            counter_text = text_manager.render_sub_text(f"Coins: {self.coin_counter[0]}")
            window.blit(counter_text, (game_width - counter_text.get_width() - 10, 10))
            
            if not self.game_over:
                self.pause_manager.draw_pause_button(window)
    
    def handle_pause_click(self, mouse_pos):  # Function to handle pause button clicks
        """Handle pause-related clicks"""
        return self.pause_manager.handle_click(mouse_pos)
    
    def update_pause(self):  # Function to update pause countdown
        """Update pause countdown"""
        return self.pause_manager.update_countdown(self.input_manager)
    
    def handle_game_over(self):  # Function to handle game over logic
        """Update high score if current score is higher"""
        if self.score > self.high_score:
            self.high_score = self.score
            save_high_score(self.high_score)