import pygame

# our code files
import behavior
import level

# Player state data
class Player:
    def __init__(self, pos=pygame.Rect(0, 0, 32, 32)):
        # position
        self.pos = pos

        # properties
        self.speed = 5

class Principle:
    def __init__(self, pos=pygame.Rect(0, 0, 32, 32)):
        # position
        self.pos = pos

        # current target location for pathfinding
        self.target = pygame.Vector2(0, 0)

        # state (0 = roam, 1 = patrol, 2 = chase)
        self.stage = 0
        self.stunned = False

        # properties
        self.speed = 4


def rect_overlap(r1, r2):
    return (min(r1.x + r1.width, r2.x + r2.width) - max(r1.x, r2.x), min(r1.y + r1.height, r2.y + r2.height) - max(r1.y, r2.y))

if __name__ == "__main__":
    # print behavior tree for inspection
    behavior_tree = behavior.create_behavior_tree()
    print(behavior_tree.tree_to_string())

    # start game
    pygame.init()

    # core setup
    window_width = 1280
    window_height = 720
    
    screen = pygame.display.set_mode((window_width, window_height), flags=pygame.SCALED, vsync=1)
    clock = pygame.time.Clock()

    # game data
    camera = pygame.Vector2(0, 0)
    
    player = Player(pygame.Rect(50, 50, 32, 32))
    principle = Principle()

    lvl = level.Level("assets/level.json", tile_size=32)

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

        # check for player collision
        tl = lvl.coord_to_tile(player.pos.x, player.pos.y)
        br = lvl.coord_to_tile(player.pos.x + player.pos.width, player.pos.y + player.pos.height)

        # loop over all tiles the player is touching, checking collision with each
        for y in range(tl[1], br[1] + 1):
            for x in range(tl[0], br[0] + 1):
                collision = False

                # we are colliding with a solid wall tile
                # TODO: Remove hard-coded tile type checks, use LDtk features instead
                if lvl.tiles[y][x].t == 0:
                    collision = True

                # resolve collision
                if collision:
                    tile_rect = pygame.Rect(x * lvl.tile_size, y * lvl.tile_size, lvl.tile_size, lvl.tile_size)
                    overlap = rect_overlap(player.pos, tile_rect)

                    # vertical resolution
                    if overlap[0] > overlap[1]:
                        # if player vertical midpoint is at or above tile vertical midpoint, resolve up
                        if player.pos.y + (player.pos.height / 2) <= tile_rect.y + (tile_rect.height / 2):
                            player.pos.y = tile_rect.y - player.pos.height
                        # resolve down
                        else:
                            player.pos.y = tile_rect.y + tile_rect.height
                    # horizontal resolution
                    else:
                        # if player horizontal midpoint is at or left of tile horizontal midpoint, resolve left
                        if player.pos.x + (player.pos.width / 2) <= tile_rect.x + (tile_rect.width / 2):
                            player.pos.x = tile_rect.x - player.pos.width
                        # resolve right
                        else:
                            player.pos.x = tile_rect.x + tile_rect.width

        # update camera pos
        camera = pygame.Vector2(player.pos.x, player.pos.y) - pygame.Vector2(window_width / 2, window_height / 2)

        # lock camera view to level
        if camera.x < 0:
            camera.x = 0
        elif camera.x + window_width > (lvl.width * lvl.tile_size):
            camera.x = (lvl.width * lvl.tile_size) - window_width

        if camera.y < 0:
            camera.y = 0
        elif camera.y + window_height > (lvl.height * lvl.tile_size):
            camera.y = (lvl.height * lvl.tile_size) - window_height

        # clear the screen with a purple color
        screen.fill("black")

        # draw level
        for y in range(0, lvl.height):
            for x in range(0, lvl.width):
                r = pygame.Rect(x * lvl.tile_size - camera.x, y * lvl.tile_size - camera.y, lvl.tile_size, lvl.tile_size)

                tile = lvl.tiles[y][x]

                # TODO: Switch to using the information from LDtk to render proper tile texture
                if tile.t == 0:
                    pygame.draw.rect(screen, "purple", r)
                elif tile.t == 1:
                    pygame.draw.rect(screen, "blue", r)
                else:
                    print("UNKNOWN TILE:", tile.t)

        # draw player
        pygame.draw.rect(screen, "green", pygame.Rect(player.pos.x - camera.x, player.pos.y - camera.y, player.pos.width, player.pos.height))

        # swap buffers
        pygame.display.flip()

        # limit FPS to 60
        clock.tick(60)

    pygame.quit()
