import pygame

# Player state data
class Player:
    def __init__(self):
        # position
        self.pos = pygame.Vector2(0, 0)

        # properties
        self.speed = 5

class Principle:
    def __init__(self):
        # position
        self.pos = pygame.Vector2(0, 0)

        # properties
        self.speed = 4

if __name__ == "__main__":
    pygame.init()

    # core setup
    screen = pygame.display.set_mode((1280, 720), flags=pygame.SCALED, vsync=1)
    clock = pygame.time.Clock()

    # game data
    player = Player()
    principle = Principle()

    up = False
    down = False
    left = False
    right = False
    
    running = True

    # game loop
    while running:
        # process OS events
        for event in pygame.event.get():
            # window closed
            if event.type == pygame.QUIT:
                running = False

        # process input
        keys = pygame.key.get_pressed()

        up = keys[pygame.K_UP]
        down = keys[pygame.K_DOWN]
        left = keys[pygame.K_LEFT]
        right = keys[pygame.K_RIGHT]

        # process player movement
        if up:
            player.pos.y -= player.speed
        if down:
            player.pos.y += player.speed
        if left:
            player.pos.x -= player.speed
        if right:
            player.pos.x += player.speed

        # clear the screen with a purple color
        screen.fill("black")

        # draw player
        pygame.draw.circle(screen, "green", player.pos, 40)

        # swap buffers
        pygame.display.flip()

        # limit FPS to 60
        clock.tick(60)

    pygame.quit()
