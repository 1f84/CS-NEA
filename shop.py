import pygame
import os

class ShopManager:
    def __init__(self, game_width, game_height, text_manager):
        self.game_width = game_width
        self.game_height = game_height
        self.text_manager = text_manager
        self.coin_file = "total_coins.txt"
        self.total_coins = self.load_total_coins()
    
    def load_total_coins(self):
        if os.path.exists(self.coin_file):
            try:
                with open(self.coin_file, 'r') as f:
                    return int(f.read().strip())
            except:
                return 0
        return 0

    def save_total_coins(self):
        with open(self.coin_file, 'w') as f:
            f.write(str(self.total_coins))
    
    def add_coins(self, coins):
        self.total_coins += coins
        self.save_total_coins()
    
    def update_total_coins(self, coins):
        self.total_coins = coins
    
    def draw(self, window, back_button):
        # Draw shop background
        window.fill((255, 255, 255))  # White background
        
        # Draw back button
        pygame.draw.rect(window, (255, 0, 0), back_button)
        back_txt = self.text_manager.render_button_text("Back", (255, 255, 255))
        window.blit(back_txt, (back_button.centerx - back_txt.get_width() // 2, back_button.centery - back_txt.get_height() // 2))
        
        # Draw shop title
        shop_title = self.text_manager.render_title("Shop")
        window.blit(shop_title, (self.game_width // 2 - shop_title.get_width() // 2, 100))
        
        # Draw total coins
        coins_text = self.text_manager.render_sub_text(f"Total Coins: {self.total_coins}")
        window.blit(coins_text, (self.game_width // 2 - coins_text.get_width() // 2, 200))
        
        # Draw upgrade cube on the left side below total coins
        cube_size = 50  # Same size as player
        cube_x = 50  # Left side of screen
        cube_y = 300  # Below total coins
        
        # Layer 1: Black outer border
        border_thickness = 2
        pygame.draw.rect(window, (0, 0, 0), (cube_x, cube_y, cube_size, cube_size))
        
        # Layer 2: Cyan layer
        cyan_layer_size = cube_size - border_thickness * 2
        cyan_layer_x = cube_x + border_thickness
        cyan_layer_y = cube_y + border_thickness
        pygame.draw.rect(window, (34, 240, 255), (cyan_layer_x, cyan_layer_y, cyan_layer_size, cyan_layer_size))
        
        # Layer 3: Thick black inner border (thickest layer)
        inner_border_thickness = 6  # Made this thicker
        black_inner_size = cyan_layer_size - inner_border_thickness * 2
        black_inner_x = cyan_layer_x + inner_border_thickness
        black_inner_y = cyan_layer_y + inner_border_thickness
        pygame.draw.rect(window, (0, 0, 0), (black_inner_x, black_inner_y, black_inner_size, black_inner_size))
        
        # Layer 4: Cyan core/middle
        core_size = black_inner_size - inner_border_thickness * 2
        core_x = black_inner_x + inner_border_thickness
        core_y = black_inner_y + inner_border_thickness
        pygame.draw.rect(window, (34, 240, 255), (core_x, core_y, core_size, core_size))
        
        # Draw price text below the cube
        price_text = self.text_manager.render_sub_text("Price: 20")
        window.blit(price_text, (cube_x + cube_size // 2 - price_text.get_width() // 2, cube_y + cube_size + 10))
    
    def update_total_coins(self, coins):
        self.total_coins = coins