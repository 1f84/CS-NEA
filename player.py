import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 5
        self.jumping = False
        self.jump_speed = -12
        self.gravity = 1
        self.velocity = 0

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += self.speed
        if self.x + self.width > 800:
            self.x = 800 - self.width

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.y_velocity = self.jump_speed

    def update(self):
        if self.jumping:
            self.y += self.y_velocity
            self.y_velocity += self.gravity
            if self.y >= 500:
                self.y = 500
                self.jumping = False
                self.y_velocity = 0

player = Player(360, 500)

move_mapping = {
    pygame.K_LEFT: player.move_left,
    pygame.K_RIGHT: player.move_right,
    pygame.K_SPACE: player.jump
}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    for key, action in move_mapping.items():
        if keys[key]:
            action()

    player.update()


    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (255, 0, 0), (player.x, player.y, player.width, player.height))

    pygame.draw.line(screen, (0, 255, 0), (0, 550), (800, 550), 3)

    pygame.display.flip()
    clock.tick(60)