import pygame

class DeathManager:
    def __init__(self, game_width, game_height, text_manager):
        self.game_width = game_width
        self.game_height = game_height
        self.text_manager = text_manager
        
        # Create death screen buttons
        self.replay_button = pygame.Rect(game_width // 2 - 100, game_height // 2 + 50, 200, 50)
        self.menu_button = pygame.Rect(game_width // 2 - 100, game_height // 2 + 120, 200, 50)
    
    def draw(self, window, coins_collected):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.game_width, self.game_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        window.blit(overlay, (0, 0))
        
        # Draw "Game Over" title
        game_over_text = self.text_manager.render_game_over("Game Over!")
        window.blit(game_over_text, (self.game_width // 2 - game_over_text.get_width() // 2, self.game_height // 2 - 100))
        
        # Draw coins collected this round
        coins_text = self.text_manager.render_sub_text(f"Coins Collected: {coins_collected}")
        window.blit(coins_text, (self.game_width // 2 - coins_text.get_width() // 2, self.game_height // 2 - 20))
        
        # Draw replay button
        pygame.draw.rect(window, (0, 255, 0), self.replay_button)
        replay_txt = self.text_manager.render_button_text("Replay")
        window.blit(replay_txt, (self.replay_button.centerx - replay_txt.get_width() // 2, self.replay_button.centery - replay_txt.get_height() // 2))
        
        # Draw main menu button
        pygame.draw.rect(window, (0, 0, 255), self.menu_button)
        menu_txt = self.text_manager.render_button_text("Main Menu")
        window.blit(menu_txt, (self.menu_button.centerx - menu_txt.get_width() // 2, self.menu_button.centery - menu_txt.get_height() // 2))
    
    def handle_click(self, mouse_pos):
        if self.replay_button.collidepoint(mouse_pos):
            return 'replay'
        elif self.menu_button.collidepoint(mouse_pos):
            return 'menu'
        return None