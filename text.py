import pygame

class TextManager:
    def __init__(self, game_Width, game_Height):
        self.game_Width = game_Width
        self.game_Height = game_Height
        self.font = pygame.font.SysFont("Arial", 36)
        self.small_font = pygame.font.SysFont("Arial", 28)
        self.large_font = pygame.font.SysFont("Arial", 48)
        self.volume_text = "Volume: 50%"  # placeholder

    def get_buttons(self):
        start_button = pygame.Rect(self.game_Width // 2 - 100, self.game_Height // 2 - 80, 200, 50)
        shop_button = pygame.Rect(self.game_Width // 2 - 100, self.game_Height // 2 - 20, 200, 50)
        settings_button = pygame.Rect(self.game_Width // 2 - 100, self.game_Height // 2 + 40, 200, 50)
        back_button = pygame.Rect(50, 50, 100, 50)
        return start_button, shop_button, settings_button, back_button

    def draw_menu(self, window):
        start_button, shop_button, settings_button, back_button = self.get_buttons()
        
        # Draw title
        title = self.render_title("Pixel Rush")
        window.blit(title, (self.game_Width // 2 - title.get_width() // 2, 100))
        
        # Draw start button
        pygame.draw.rect(window, (0, 255, 0), start_button)
        start_txt = self.render_button_text("Start")
        window.blit(start_txt, (start_button.centerx - start_txt.get_width() // 2, start_button.centery - start_txt.get_height() // 2))
        
        # Draw shop button
        pygame.draw.rect(window, (255, 215, 0), shop_button)  # Gold color
        shop_txt = self.render_button_text("Shop", (0, 0, 0))
        window.blit(shop_txt, (shop_button.centerx - shop_txt.get_width() // 2, shop_button.centery - shop_txt.get_height() // 2))
        
        # Draw settings button
        pygame.draw.rect(window, (0, 0, 255), settings_button)
        settings_txt = self.render_button_text("Settings", (255, 255, 255))
        window.blit(settings_txt, (settings_button.centerx - settings_txt.get_width() // 2, settings_button.centery - settings_txt.get_height() // 2))

    def draw_settings(self, window):
        start_button, shop_button, settings_button, back_button = self.get_buttons()
        
        # Draw settings background
        window.fill((255, 255, 255))  # White background
        
        # Draw settings title
        settings_title = self.render_title("Settings")
        window.blit(settings_title, (self.game_Width // 2 - settings_title.get_width() // 2, 100))
        
        # Draw volume text
        vol_txt = self.render_title(self.volume_text)
        window.blit(vol_txt, (self.game_Width // 2 - vol_txt.get_width() // 2, self.game_Height // 2))
        
        # Draw back button
        pygame.draw.rect(window, (255, 0, 0), back_button)
        back_txt = self.render_button_text("Back", (255, 255, 255))
        window.blit(back_txt, (back_button.centerx - back_txt.get_width() // 2, back_button.centery - back_txt.get_height() // 2))

    def render_title(self, text, color=(0, 0, 0)):
        return self.font.render(text, True, color)

    def render_button_text(self, text, color=(0, 0, 0)):
        return self.font.render(text, True, color)

    def render_game_over(self, text, color=(0, 0, 0)):
        return self.large_font.render(text, True, color)

    def render_sub_text(self, text, color=(0, 0, 0)):
        return self.small_font.render(text, True, color)
