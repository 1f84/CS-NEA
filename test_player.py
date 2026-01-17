import pygame
from player import Player

pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test Player")
clock = pygame.time.Clock()

ground_y = 550
player = Player(375, ground_y - 50, 50, 50, 8)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # optional: use KEYDOWN for single-press actions
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # per-frame input (for smooth movement)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right(window.get_width())

    # update physics every frame
    player.update(ground_y)

    # draw every frame
    window.fill((255, 255, 255))
    player.draw(window)
    pygame.display.update()
    clock.tick(60)

pygame.quit()

