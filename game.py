import time

class GameManager:
    def __init__(self, player, obstacle_manager, coin_manager, input_manager, shop_manager, pause_manager):
        self.player = player
        self.obstacle_manager = obstacle_manager
        self.coin_manager = coin_manager
        self.input_manager = input_manager
        self.shop_manager = shop_manager
        self.pause_manager = pause_manager
        
        self.game_over = False
        self.coin_counter = [0]
        self.game_start_time = 0
        self.last_speed_increase = 0
        self.current_obstacle_speed = 6  # Starting speed
        self.speed_increase_interval = 15  # seconds
    
    def reset_game(self, game_width, ground_y):
        """Reset game state for a new game"""
        self.game_over = False
        self.pause_manager.reset()
        self.player.x, self.player.y = game_width // 2 - 25, ground_y - self.player.height
        self.obstacle_manager.obstacles.clear()
        self.obstacle_manager.spawn_timer = 0
        self.coin_manager.coins.clear()
        self.coin_manager.spawn_timer = 0
        self.coin_counter[0] = 0
        self.input_manager.last_move_time = time.time()
        self.player.vel_y = 0
        self.player.jumping = False
        # Reset speed progression
        self.game_start_time = time.time()
        self.last_speed_increase = 0
        self.current_obstacle_speed = 6
    
    def update_game(self, game_width, game_height, obstacle_color, ground_y):
        """Update game logic (only when not paused)"""
        if self.game_over or self.pause_manager.paused:
            return
        
        # Update speed progression
        current_time = time.time() - self.game_start_time
        speed_level = int(current_time // self.speed_increase_interval)
        if speed_level > self.last_speed_increase:
            self.current_obstacle_speed += 1  # Increase speed by 1 every 15 seconds
            self.last_speed_increase = speed_level
        
        action = self.input_manager.handle(self.player, game_width, self.game_over)
        
        # Check for inactivity timeout
        if time.time() - self.input_manager.last_move_time > 5:
            self.game_over = True
            self.shop_manager.add_coins(self.coin_counter[0])
            return
        
        self.player.update(ground_y)
        
        # Check for collisions
        if self.obstacle_manager.update(self.player, game_width, game_height, self.current_obstacle_speed, obstacle_color):
            self.game_over = True
            self.shop_manager.add_coins(self.coin_counter[0])
            return
        
        self.coin_manager.update(self.player, game_width, game_height, self.current_obstacle_speed, self.coin_counter)
    
    def draw_game(self, window, text_manager, game_width):
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
    
    def handle_pause_click(self, mouse_pos):
        """Handle pause-related clicks"""
        return self.pause_manager.handle_click(mouse_pos)
    
    def update_pause(self):
        """Update pause countdown"""
        return self.pause_manager.update_countdown(self.input_manager)