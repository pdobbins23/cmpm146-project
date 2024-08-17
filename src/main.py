import pygame

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    running = True

    while running:
        # process OS events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # clear the screen with a purple color
        screen.fill("purple")

        pygame.display.flip()

        # limit FPS to 60
        clock.tick(60)

    pygame.quit()
