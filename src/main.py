import pygame
# our code files
import behavior

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
    # print behavior tree for inspection
    behavior_tree = behavior.create_behavior_tree()
    print(behavior_tree.tree_to_string())

    # start game
    pygame.init()

    # core setup
    screen = pygame.display.set_mode((1280, 720), flags=pygame.SCALED, vsync=1)
    clock = pygame.time.Clock()

    # game data
    player = Player()
    principle = Principle()
    
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

        # process player movement
        if keys[pygame.K_UP]:
            player.pos.y -= player.speed
        if keys[pygame.K_DOWN]:
            player.pos.y += player.speed
        if keys[pygame.K_LEFT]:
            player.pos.x -= player.speed
        if keys[pygame.K_RIGHT]:
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
