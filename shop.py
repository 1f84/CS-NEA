import pygame  # Importing pygame library to help me code my game.
import os      # Importing os library for file operations.

class ShopManager:  # ShopManager class to handle shop functionality and coin management
    def __init__(self, game_width, game_height, text_manager, player):  # Initialising shop manager attributes
        self.game_width = game_width      # Game window width
        self.game_height = game_height    # Game window height
        self.text_manager = text_manager  # Text manager for rendering text
        self.player = player              # Player object
        self.coin_file = "total_coins.txt"  # File to store total coins
        self.skin_file = "skin_data.txt"  # File to store skin data
        self.total_coins = self.load_total_coins()  # Load total coins from file
        self.skin_owned = False           # Whether the skin is owned
        self.skin_equipped = False        # Whether the skin is equipped
        self.load_skin_data()             # Load skin data from file
        self.default_color = (50, 150, 250)  # Default player color
        self.skin_color = (34, 240, 255)     # Skin color
        self.update_player_color()        # Update player's color based on equipped skin
    
    def load_total_coins(self):  # Function to load total coins from file
        if os.path.exists(self.coin_file):
            try:
                with open(self.coin_file, 'r') as f:
                    return int(f.read().strip())
            except:
                return 0
        return 0

    def save_total_coins(self):  # Function to save total coins to file
        with open(self.coin_file, 'w') as f:
            f.write(str(self.total_coins))
    
    def load_skin_data(self):  # Function to load skin data from file
        if os.path.exists(self.skin_file):
            with open(self.skin_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("owned:"):
                        self.skin_owned = line.strip().split(":")[1] == "True"
                    elif line.startswith("equipped:"):
                        self.skin_equipped = line.strip().split(":")[1] == "True"
    
    def save_skin_data(self):  # Function to save skin data to file
        with open(self.skin_file, 'w') as f:
            f.write(f"owned:{self.skin_owned}\n")
            f.write(f"equipped:{self.skin_equipped}\n")
    
    def update_player_color(self):  # Function to update player's color based on equipped skin
        if self.skin_equipped:
            self.player.color = self.skin_color
            self.player.is_skin_equipped = True
        else:
            self.player.color = self.default_color
            self.player.is_skin_equipped = False
    
    def add_coins(self, coins):  # Function to add coins to total
        self.total_coins += coins
        self.save_total_coins()
    
    def update_total_coins(self, coins):  # Function to update total coins
        self.total_coins = coins
    
    def draw(self, window, back_button):  # Function to draw the shop screen
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
        
        # Layer 1: Black outer border for the cube outline
        border_thickness = 2
        pygame.draw.rect(window, (0, 0, 0), (cube_x, cube_y, cube_size, cube_size))
        
        # Layer 2: Cyan layer inside the border
        cyan_layer_size = cube_size - border_thickness * 2
        cyan_layer_x = cube_x + border_thickness
        cyan_layer_y = cube_y + border_thickness
        pygame.draw.rect(window, (34, 240, 255), (cyan_layer_x, cyan_layer_y, cyan_layer_size, cyan_layer_size))
        
        # Layer 3: Thick black inner border to create depth
        inner_border_thickness = 6  # Made this thicker for emphasis
        black_inner_size = cyan_layer_size - inner_border_thickness * 2
        black_inner_x = cyan_layer_x + inner_border_thickness
        black_inner_y = cyan_layer_y + inner_border_thickness
        pygame.draw.rect(window, (0, 0, 0), (black_inner_x, black_inner_y, black_inner_size, black_inner_size))
        
        # Layer 4: Cyan core in the center for the final effect
        core_size = black_inner_size - inner_border_thickness * 2
        core_x = black_inner_x + inner_border_thickness
        core_y = black_inner_y + inner_border_thickness
        pygame.draw.rect(window, (34, 240, 255), (core_x, core_y, core_size, core_size))
        
        # Draw price text below the cube
        price_text = self.text_manager.render_sub_text("Price: 20")
        window.blit(price_text, (cube_x + cube_size // 2 - price_text.get_width() // 2, cube_y + cube_size + 10))
        
        # Draw button below price
        button_y = cube_y + cube_size + 40
        button_width = 100
        button_height = 30
        button_x = cube_x + cube_size // 2 - button_width // 2
        self.skin_button = pygame.Rect(button_x, button_y, button_width, button_height)  # Skin button rect
        if not self.skin_owned:
            button_text = "Buy"
            button_color = (0, 255, 0)  # Green for buy
        else:
            if self.skin_equipped:
                button_text = "Unequip"
                button_color = (255, 255, 0)  # Yellow for unequip
            else:
                button_text = "Equip"
                button_color = (0, 255, 0)  # Green for equip
        pygame.draw.rect(window, button_color, self.skin_button)
        btn_txt = self.text_manager.render_button_text(button_text, (0, 0, 0))
        window.blit(btn_txt, (self.skin_button.centerx - btn_txt.get_width() // 2, self.skin_button.centery - btn_txt.get_height() // 2))
    
    def handle_click(self, mouse_pos):  # Function to handle clicks in the shop
        if self.skin_button.collidepoint(mouse_pos):
            if not self.skin_owned:
                if self.total_coins >= 20:
                    self.total_coins -= 20
                    self.save_total_coins()
                    self.skin_owned = True
                    self.skin_equipped = True  # Auto equip after buying
                    self.save_skin_data()
                    self.update_player_color()
            else:
                self.skin_equipped = not self.skin_equipped
                self.save_skin_data()
                self.update_player_color()
    
    def add_coins(self, coins):  # Function to add coins to total
        self.total_coins += coins
        self.save_total_coins()
    
    def update_total_coins(self, coins):  # Function to update total coins
        self.total_coins = coins