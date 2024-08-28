import pygame
import random

# our code files
import behavior
import level
from helper_functions import a_star

# Player state data
class Player:
    def __init__(self, pos=pygame.Rect(0, 0, 32, 32)):
        # position
        self.pos = pos
        self.dir = 0

        # item
        self.holding_item = None
        self.throw_speed = 10

        # hiding in locker
        self.locker = None

        # properties
        self.speed = 5

class Principle:
    def __init__(self, pos=pygame.Rect(0, 0, 32, 32)):
        # position
        self.pos = pos

        # current target location for pathfinding
        self.target = None

        # current pathfinding path
        self.path = None

        # state (0 = roam, 1 = patrol, 2 = chase)
        self.stage = 0
        self.health = 10

        # properties
        self.speed = 4

class Item:
    def __init__(self, pos=pygame.Rect(0, 0, 16, 16)):
        self.pos = pos
        self.vel = pygame.Vector2(0, 0)

def rect_overlap(r1, r2):
    return (min(r1.x + r1.width, r2.x + r2.width) - max(r1.x, r2.x), min(r1.y + r1.height, r2.y + r2.height) - max(r1.y, r2.y))

if __name__ == "__main__":
    # print behavior tree for inspection
    # behavior_tree = behavior.create_behavior_tree()
    # print(behavior_tree.tree_to_string())

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
    principle = Principle(pygame.Rect(100, 100, 32, 32))

    lvl = level.Level("assets/demo_level.json.ldtk", tile_size=32)

    items = []

    # generate items
    for y in range(0, lvl.height):
        for x in range(0, lvl.width):
            if lvl.tiles[y][x].t == 1 and random.random() < 0.01:
                items.append(Item(pygame.Rect(x * lvl.tile_size, y * lvl.tile_size, 16, 16)))

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
            player.dir = 0
            player.pos.y -= player.speed
        if keys[pygame.K_DOWN]:
            player.dir = 1
            player.pos.y += player.speed
        if keys[pygame.K_LEFT]:
            player.dir = 2
            player.pos.x -= player.speed
        if keys[pygame.K_RIGHT]:
            player.dir = 3
            player.pos.x += player.speed

        if keys[pygame.K_SPACE] and player.holding_item != None:
            if player.dir == 0:
                items[player.holding_item].vel = pygame.Vector2(0, -player.throw_speed)
            elif player.dir == 1:
                items[player.holding_item].vel = pygame.Vector2(0, player.throw_speed)
            elif player.dir == 2:
                items[player.holding_item].vel = pygame.Vector2(-player.throw_speed, 0)
            elif player.dir == 3:
                items[player.holding_item].vel = pygame.Vector2(player.throw_speed, 0)

            player.holding_item = None

        # process items
        for i, item in enumerate(items):
            collision = rect_overlap(item.pos, player.pos)

            if item.vel.x == 0 and item.vel.y == 0 and player.holding_item == None and collision[0] > 0 and collision[1] > 0:
                player.holding_item = i
            
            if player.holding_item == i:
                item.pos.x = player.pos.x + player.pos.width / 2 - item.pos.width / 2
                item.pos.y = player.pos.y + player.pos.height / 2 - item.pos.height / 2

                if player.dir == 0:
                    item.pos.y -= player.pos.height
                elif player.dir == 1:
                    item.pos.y += player.pos.height
                elif player.dir == 2:
                    item.pos.x -= player.pos.width
                elif player.dir == 3:
                    item.pos.x += player.pos.width

            if item.vel.x != 0 or item.vel.y != 0:
                # item moving
                item.pos = pygame.Rect(item.pos.x + item.vel.x, item.pos.y + item.vel.y, item.pos.width, item.pos.height)

                item.vel.x *= 0.95
                item.vel.y *= 0.95

                if abs(item.vel.x) < 0.1 and abs(item.vel.y) < 0.1:
                    item.vel.x = 0
                    item.vel.y = 0

                # principle collision
                principle_collision = rect_overlap(item.pos, principle.pos)

                if principle_collision[0] > 0 and principle_collision[1] > 0:
                    principle.health -= 1

                    item.vel.x *= -0.35
                    item.vel.y *= -0.35

            # item collision
            tl = lvl.coord_to_tile(item.pos.x, item.pos.y)
            br = lvl.coord_to_tile(item.pos.x + item.pos.width, item.pos.y + item.pos.height)

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
                        overlap = rect_overlap(item.pos, tile_rect)

                        # vertical resolution
                        if overlap[0] > overlap[1]:
                            # if item vertical midpoint is at or above tile vertical midpoint, resolve up
                            if item.pos.y + (item.pos.height / 2) <= tile_rect.y + (tile_rect.height / 2):
                                item.pos.y = tile_rect.y - item.pos.height
                                # bounce
                                item.vel.y *= -0.35
                            # resolve down
                            else:
                                item.pos.y = tile_rect.y + tile_rect.height
                                # bounce
                                item.vel.y *= -0.35
                        # horizontal resolution
                        else:
                            # if item horizontal midpoint is at or left of tile horizontal midpoint, resolve left
                            if item.pos.x + (item.pos.width / 2) <= tile_rect.x + (tile_rect.width / 2):
                                item.pos.x = tile_rect.x - item.pos.width
                                # bounce
                                item.vel.x *= -0.35
                            # resolve right
                            else:
                                item.pos.x = tile_rect.x + tile_rect.width
                                # bounce
                                item.vel.x *= -0.35

        # process principle
        # TODO: Invoke behavior tree with current state

        # pathfind to current principle target
        principle.target = player.pos
        
        # Pathfinding logic
        if principle.target:
            # Convert principle's target to tuple for a_star
            target_pos = (principle.target.x, principle.target.y)
            principle.path = a_star((principle.pos.x, principle.pos.y), target_pos, lvl.tiles)

            print(principle.path)

        # follow path logic
        if principle.path:
            # Move principle towards the next point in the path
            next_point = principle.path[0]
            direction = pygame.Vector2(next_point[0] - principle.pos.x, next_point[1] - principle.pos.y).normalize()
            principle.pos.x += direction.x * principle.speed
            principle.pos.y += direction.y * principle.speed

            # Check if principle has reached the next point
            if pygame.math.Vector2(principle.pos.x, principle.pos.y).distance_to(pygame.math.Vector2(next_point[0], next_point[1])) < principle.speed:
                # Remove the reached point from the path
                path.pop(0)
                if path:
                    next_point = path[0]
                else:
                    principle.target = None

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

        # draw principle
        pygame.draw.rect(screen, "red", pygame.Rect(principle.pos.x - camera.x, principle.pos.y - camera.y, principle.pos.width, principle.pos.height))

        # draw items
        for item in items:
            pygame.draw.rect(screen, "brown", pygame.Rect(item.pos.x - camera.x, item.pos.y - camera.y, item.pos.width, item.pos.height))

        # swap buffers
        pygame.display.flip()

        # limit FPS to 60
        clock.tick(60)

    pygame.quit()
