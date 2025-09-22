import pygame
import sys
from player import Player

game_Width = 600
game_Height = 800

pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pixel rush")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)
