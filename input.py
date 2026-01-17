import pygame  # Importing pygame library to help me code my game.
import time    # Importing time library for timing functions.

class InputManager:  # InputManager class to handle user input
    def __init__(self):  # Initialising input manager attributes
        self.last_move_time = time.time()  # Track the last time left or right was pressed for inactivity timeout
        self.prev_keys = {pygame.K_LEFT: False, pygame.K_RIGHT: False}  # Track previous key states
    
    def handle(self, player, game_Width, game_over):  # Function to handle keyboard input
        keys = pygame.key.get_pressed()
        
        if game_over:
            if keys[pygame.K_r]:
                return 'restart'
        else:
            # Update last move time if left or right is pressed
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                self.last_move_time = time.time()
            
            # Handle left movement
            if keys[pygame.K_LEFT]:
                if not self.prev_keys[pygame.K_LEFT]:  # Key just pressed (tap)
                    player.move_left_tap()
                else:  # Key held down
                    player.move_left()
            elif self.prev_keys[pygame.K_LEFT]:  # Key just released
                pass
            
            # Handle right movement
            if keys[pygame.K_RIGHT]:
                if not self.prev_keys[pygame.K_RIGHT]:  # Key just pressed (tap)
                    player.move_right_tap(game_Width)
                else:  # Key held down
                    player.move_right(game_Width)
            elif self.prev_keys[pygame.K_RIGHT]:  # Key just released
                pass
            
            if keys[pygame.K_SPACE]:
                player.jump()
        
        # Update previous key states
        self.prev_keys[pygame.K_LEFT] = keys[pygame.K_LEFT]
        self.prev_keys[pygame.K_RIGHT] = keys[pygame.K_RIGHT]
        
        return None
