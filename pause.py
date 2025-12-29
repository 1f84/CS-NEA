import pygame
import time

class PauseManager:
    def __init__(self, game_width, game_height, text_manager):
        self.game_width = game_width
        self.game_height = game_height
        self.text_manager = text_manager
        
        # Pause UI elements
        self.pause_button = pygame.Rect(10, 10, 80, 40)
        self.resume_button = pygame.Rect(game_width // 2 - 100, game_height // 2 - 25, 200, 50)
        
        # Pause state
        self.paused = False
        self.countdown_active = False
        self.countdown_start_time = 0
        self.countdown_duration = 3  # 3 seconds
    
    def toggle_pause(self):
        """Toggle pause state"""
        if not self.paused:
            self.paused = True
        elif not self.countdown_active:
            self.start_resume_countdown()
    
    def start_resume_countdown(self):
        """Start the resume countdown"""
        self.countdown_active = True
        self.countdown_start_time = time.time()
    
    def update_countdown(self, input_manager):
        """Update countdown and return True if countdown finished"""
        if self.countdown_active:
            elapsed = time.time() - self.countdown_start_time
            remaining = self.countdown_duration - elapsed
            if remaining <= 0:
                self.paused = False
                self.countdown_active = False
                input_manager.last_move_time = time.time()  # Reset inactivity timer
                return True
        return False
    
    def draw_pause_button(self, window):
        """Draw the pause button"""
        pygame.draw.rect(window, (255, 0, 0), self.pause_button)
        pause_txt = self.text_manager.render_button_text("Pause", (255, 255, 255))
        window.blit(pause_txt, (self.pause_button.centerx - pause_txt.get_width() // 2, 
                               self.pause_button.centery - pause_txt.get_height() // 2))
    
    def draw_paused_screen(self, window, player, obstacle_manager, coin_manager, coin_counter):
        """Draw the paused game state"""
        # Draw frozen game elements
        player.draw(window)
        for obstacle in obstacle_manager.obstacles:
            obstacle.draw(window)
        for coin in coin_manager.coins:
            coin.draw(window)
        
        counter_text = self.text_manager.render_sub_text(f"Coins: {coin_counter[0]}")
        window.blit(counter_text, (self.game_width - counter_text.get_width() - 10, 10))
        
        if self.countdown_active:
            # Draw countdown
            elapsed = time.time() - self.countdown_start_time
            remaining = self.countdown_duration - elapsed
            countdown_text = self.text_manager.render_game_over(str(int(remaining) + 1))
            window.blit(countdown_text, (self.game_width // 2 - countdown_text.get_width() // 2, 
                                        self.game_height // 2 - countdown_text.get_height() // 2))
        else:
            # Draw resume button with overlay
            pygame.draw.rect(window, (0, 255, 0), self.resume_button)
            resume_txt = self.text_manager.render_button_text("Resume")
            window.blit(resume_txt, (self.resume_button.centerx - resume_txt.get_width() // 2, 
                                    self.resume_button.centery - resume_txt.get_height() // 2))
            
            # Semi-transparent overlay
            overlay = pygame.Surface((self.game_width, self.game_height))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            window.blit(overlay, (0, 0))
    
    def handle_click(self, mouse_pos):
        """Handle mouse clicks on pause UI"""
        if self.pause_button.collidepoint(mouse_pos) and not self.paused:
            self.paused = True
            return 'pause_clicked'
        elif self.resume_button.collidepoint(mouse_pos) and self.paused and not self.countdown_active:
            self.start_resume_countdown()
            return 'resume_clicked'
        return None
    
    def reset(self):
        """Reset pause state (for new games)"""
        self.paused = False
        self.countdown_active = False