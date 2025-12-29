import pygame   # Importing pygame and other necessary librarys so that I can code my game.
import sys
import random
import time
from obstacle import Obstacle, ObstacleManager
from input import InputManager
from player import Player
from text import TextManager
from coin import CoinManager
from shop import ShopManager
from death import DeathManager
from pause import PauseManager
from game import GameManager

# --- WINDOW SETUP ---
pygame.init()                                  # Initialises pygame
game_Width = 800                               # This establishes the height and width of the game window
game_Height = 600 
text_manager = TextManager(game_Width, game_Height)
window = pygame.display.set_mode((game_Width, game_Height), pygame.RESIZABLE)   # Creates a resizable game window
pygame.display.set_caption("Pixel rush")       # This sets the title of the game


WHITE = (255, 255, 255)
Player_Color = (50, 150, 250)
Obstacle_Color = (255, 60, 60)

clock = pygame.time.Clock()                    # Creates clock variable to manage the frame rate
Ground_y = game_Height - 50
running = True

# Game states
MENU = 'menu'
SETTINGS = 'settings'
GAME = 'game'
SHOP = 'shop'
state = MENU

# --- Create Player ---
player = Player(game_Width // 2 -25, Ground_y - 50, 50, 50, 8)

obstacle_manager = ObstacleManager(180)
input_manager = InputManager()
coin_manager = CoinManager(600)  # 10 seconds at 60 FPS

shop_manager = ShopManager(game_Width, game_Height, text_manager)
death_manager = DeathManager(game_Width, game_Height, text_manager)
pause_manager = PauseManager(game_Width, game_Height, text_manager)

game_manager = GameManager(player, obstacle_manager, coin_manager, input_manager, shop_manager, pause_manager)

# Button definitions
start_button, shop_button, settings_button, back_button = text_manager.get_buttons()
volume_text = text_manager.volume_text

while running:
    clock.tick(60)
    window.fill(WHITE)
    
    for event in pygame.event.get():  # This is for processing events
        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Handle window resize (including maximize/restore)
            game_Width, game_Height = event.w, event.h
            Ground_y = game_Height - 50  # Update ground level
            window = pygame.display.set_mode((game_Width, game_Height), pygame.RESIZABLE)
            text_manager = TextManager(game_Width, game_Height)  # Recreate text manager with new dimensions
            start_button, shop_button, settings_button, back_button = text_manager.get_buttons()  # Update buttons
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if state == MENU:
                if start_button.collidepoint(mouse_pos):
                    state = GAME
                    game_manager.reset_game(game_Width, Ground_y)
                elif shop_button.collidepoint(mouse_pos):
                    state = SHOP
                elif settings_button.collidepoint(mouse_pos):
                    state = SETTINGS
            elif state == SETTINGS:
                if back_button.collidepoint(mouse_pos):
                    state = MENU
            elif state == SHOP:
                if back_button.collidepoint(mouse_pos):
                    state = MENU
            elif state == GAME and game_manager.game_over:
                death_action = death_manager.handle_click(mouse_pos)
                if death_action == 'replay':
                    game_manager.reset_game(game_Width, Ground_y)
                elif death_action == 'menu':
                    state = MENU
                    game_manager.reset_game(game_Width, Ground_y)
            elif state == GAME and not game_manager.game_over and not pause_manager.paused:
                pause_action = game_manager.handle_pause_click(mouse_pos)
                if pause_action == 'pause_clicked':
                    pass  # pause_manager already handles this
            elif state == GAME and pause_manager.paused and not pause_manager.countdown_active:
                resume_action = game_manager.handle_pause_click(mouse_pos)
                if resume_action == 'resume_clicked':
                    pass  # pause_manager already handles this

    if state == MENU:
        text_manager.draw_menu(window)
    
    elif state == SETTINGS:
        text_manager.draw_settings(window)
    
    elif state == SHOP:
        shop_manager.draw(window, back_button)
    
    elif state == GAME:
        # Update game logic
        game_manager.update_game(game_Width, game_Height, Obstacle_Color, Ground_y)
        game_manager.update_pause()
        
        # Draw game
        game_manager.draw_game(window, text_manager, game_Width)
        
        # Draw death screen if game over
        if game_manager.game_over:
            death_manager.draw(window, game_manager.coin_counter[0])

    pygame.display.update()
    

pygame.quit()  # Quits pygame
sys.exit()     # Exits the programobstacle_spe