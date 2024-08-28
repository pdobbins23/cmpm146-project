import pygame
import random
import math

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
        self.throw_speed = 20

        # hiding in locker
        self.locker = None

        # properties
        self.speed = 5

class Principle:
    def __init__(self, pos=pygame.Rect(0, 0, 32, 32)):
        # position
        self.pos = pos

        # current target location for pathfinding
        self.target = (player.pos.x, player.pos.y)

        # current pathfinding path
        self.path = (player.pos.x, player.pos.y)

        # state (0 = roam, 1 = patrol, 2 = chase)
        self.stage = 0
        self.health = 10

        # properties
        self.speed = 4

class Item:
    def __init__(self, texture, pos=pygame.Rect(0, 0, 16, 16)):
        self.pos = pos
        self.vel = pygame.Vector2(0, 0)
        self.texture = texture

    def render(self, screen):
        screen.blit(self.texture, self.pos)

class Locker:
    def __init__(self, pos=pygame.Rect(0, 0, 32, 64)):
        self.pos = pos

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
            if lvl.tiles[y][x].t == 1 and random.random() < 0.005:
                random_x = random.random() * lvl.tile_size
                random_y = random.random() * lvl.tile_size
                items.append(Item(None, pygame.Rect(x * lvl.tile_size + random_x, y * lvl.tile_size + random_y, 16, 16)))

    lockers = [Locker(pygame.Rect(200, 200, 32, 64))]

    running = True

    # game loop
    while running:
        pressed_e = False
        
        # process OS events
        for event in pygame.event.get():
            # window closed
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    pressed_e = True

        # process input
        keys = pygame.key.get_pressed()

        # process player movement

        # check for collision with locker
        if player.locker == None:
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

            for i, locker in enumerate(lockers):
                collision = rect_overlap(locker.pos, player.pos)

                if collision[0] > 0 and collision[1] > 0:
                    if pressed_e:
                        player.locker = i

                    break
        else:
            if pressed_e:
                player.locker = None

        if keys[pygame.K_SPACE] and player.holding_item != None and player.locker == None:
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

                item.vel.x *= 0.9
                item.vel.y *= 0.9

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
        '''if principle.target is not None:
            print("Target is set.")
        else:
            print("Target is None.")

        principle.target = (100, 100)
        principle.path = [(50, 50), (60, 60), (70, 70)]

        if principle.path is not None:
            print("Principle has a path to follow.")
        else:
            print("Principle does not have a path.")'''

        if principle.target is not None:
            #path = helper_functions.a_star((principle.pos.x, principle.pos.y),(principle.target.x, principle.target.y),lvl.tiles)
            target_pos = principle.target
            principle.path = a_star((principle.pos.x, principle.pos.y), target_pos, lvl.tiles)
            print(principle.path) # PRINT STATEMENT CHECK

            # Follow the first step of the path if it exists
            if principle.path:
                next_step = principle.path[0]
                dx = next_step[0] - principle.pos.x
                dy = next_step[1] - principle.pos.y

                distance = math.sqrt(dx**2 + dy**2)
                if distance != 0:
                    dx, dy = dx / distance * principle.speed, dy / distance * principle.speed

                principle.pos.x += dx
                principle.pos.y += dy

                # If reached the target step, remove it from the path
                if math.hypot(principle.pos.x - next_step[0], principle.pos.y - next_step[1]) < principle.speed:
                    principle.path.pop(0)

        # pathfind to current principle target
        '''principle.target = player.pos
        
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
                    principle.target = None'''

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

        # draw lockers
        for i, locker in enumerate(lockers):
            if player.locker == i:
                pygame.draw.rect(screen, "green", pygame.Rect(locker.pos.x - camera.x - 5, locker.pos.y - camera.y - 5, locker.pos.width + 10, locker.pos.height + 10))

            pygame.draw.rect(screen, "gray", pygame.Rect(locker.pos.x - camera.x, locker.pos.y - camera.y, locker.pos.width, locker.pos.height))

        # draw player
        if player.locker == None:
            pygame.draw.rect(screen, "green", pygame.Rect(player.pos.x - camera.x, player.pos.y - camera.y, player.pos.width, player.pos.height))

        # draw principle
        pygame.draw.rect(screen, "red", pygame.Rect(principle.pos.x - camera.x, principle.pos.y - camera.y, principle.pos.width, principle.pos.height))

        # draw items
        for i, item in enumerate(items):
            if player.locker != None and i == player.holding_item:
                continue
            
            pygame.draw.rect(screen, "brown", pygame.Rect(item.pos.x - camera.x, item.pos.y - camera.y, item.pos.width, item.pos.height))

        # swap buffers
        pygame.display.flip()

        # limit FPS to 60
        clock.tick(60)

    pygame.quit()
