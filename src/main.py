import pygame
import random
import math
import time

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

class Principal:
    def __init__(self, pos=pygame.Rect(0, 0, 32, 48)):
        # position
        self.pos = pos
        self.dir = 0

        # current target location for pathfinding
        self.target = None

        # view angle (~140 degrees)
        self.viewing_angle = 2.3
        self.view_midpoint = None

        # current pathfinding path
        self.path = None

        # state (0 = roam, 1 = patrol, 2 = chase)
        self.stage = 0
        self.health = 10
        self.heard_sound = None
        self.can_see_player = False
        self.last_seen_player_pos = None
        self.last_seen_player_time = 0

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

class State:
    def __init__(self, player, principal, items, lockers, level, time):
        self.player = player
        self.principal = principal
        self.items = items
        self.lockers = lockers
        self.level = level
        self.time = time

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
    principal = Principal(pygame.Rect(100, 100, 32, 32))

    pathfind_ticks = 0

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

                    # sound
                    principal.heard_sound = (item.pos.x, item.pos.y)

                # principal collision
                principal_collision = rect_overlap(item.pos, principal.pos)

                if principal_collision[0] > 0 and principal_collision[1] > 0:
                    principal.health -= 1

                    item.vel.x *= -0.35
                    item.vel.y *= -0.35

            # item collision
            tl = lvl.coord_to_tile(item.pos.x, item.pos.y)
            br = lvl.coord_to_tile(item.pos.x + item.pos.width, item.pos.y + item.pos.height)

            # loop over all tiles the item is touching, checking collision with each
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

        # process line of sight
        principal.can_see_player = False
        
        vdx = (player.pos.x + player.pos.width / 2) - (principal.pos.x + principal.pos.width / 2)
        vdy = (player.pos.y + player.pos.height / 2) - (principal.pos.y + principal.pos.height / 2)

        player_angle = pygame.Vector2(principal.pos.x + principal.pos.width / 2, principal.pos.y + principal.pos.height / 2).angle_to(pygame.Vector2(player.pos.x + player.pos.width / 2, player.pos.y + player.pos.height / 2)) # math.atan2(vdy, vdx)

        print(player_angle)

        if principal.dir == 0:
            principal_angle = -math.pi / 2
        elif principal.dir == 1:
            principal_angle = math.pi / 2
        elif principal.dir == 2:
            principal_angle = math.pi
        elif principal.dir == 3:
            principal_angle = 0
        elif principal.dir == 4:
            principal_angle = 3 * -math.pi / 4
        elif principal.dir == 5:
            principal_angle = -math.pi / 4
        elif principal.dir == 6:
            principal_angle = 3 * math.pi / 4
        elif principal.dir == 7:
            principal_angle = math.pi / 4

        angle_diff = math.fabs(principal_angle - player_angle)

        # print(principal_angle, player_angle, angle_diff)

        # player within viewing angle
        if angle_diff <= principal.viewing_angle / 2:
            obstruction = False

            # cast ray from principal position to player, check for tile collisions
            dist = math.sqrt(vdx**2 + vdy**2)
            inc = 1

            if dist != 0:
                ddx = vdx / dist * inc
                ddy = vdy / dist * inc

                rpos = [principal.pos.x + principal.pos.width / 2, principal.pos.y + principal.pos.height / 2]

                while True:
                    rpos[0] += ddx
                    rpos[1] += ddy

                    tile = lvl.coord_to_tile(rpos[0], rpos[1])

                    if lvl.tiles[tile[1]][tile[0]].t == 0:
                        obstruction = True
                        break

                    if player.pos.collidepoint(rpos[0], rpos[1]):
                        break

            principal.view_midpoint = rpos

            if not obstruction:
                principal.can_see_player = True

        if principal.can_see_player:
            principal.last_seen_player_pos = (player.pos.x, player.pos.y)
            principal.last_seen_player_time = time.time()

        # process principal
        state = State(player, principal, items, lockers, lvl, time.time())

        # result = behavior_tree.execute(state)

        # print("BEHAVIOR:", result)

        pathfind_ticks += 1

        # if principal.stage == 0:
            # print("ROAMING")
        # if principal.stage == 1:
            # print("PATROLLING")
        # if principal.stage == 2:
            # print("CHASING")

        if pathfind_ticks > 0:
            pathfind_ticks = 0
            principal.target = (player.pos.x + player.pos.width / 2, player.pos.y + player.pos.height / 2)

        # pathfinding
        if principal.target != None:
            principal.path = a_star(lvl, (principal.pos.x, principal.pos.y), principal.target)
            # print(principal.target, principal.path) # PRINT STATEMENT CHECK
            principal.target = None

        # Follow the first step of the path if it exists
        if principal.path:
            next_step = principal.path[0]

            dx = next_step[0] - (principal.pos.x + principal.pos.width / 2)
            dy = next_step[1] - (principal.pos.y + principal.pos.height / 2)

            distance = math.sqrt(dx**2 + dy**2)
            if distance != 0:
                dx, dy = dx / distance * principal.speed, dy / distance * principal.speed

            # print(dx, dy, distance, principal.path)

            if dx < 0:
                if dy < 0:
                    principal.dir = 4
                elif dy > 0:
                    principal.dir = 6
                else:
                    principal.dir = 2
            elif dx > 0:
                if dy < 0:
                    principal.dir = 5
                elif dy > 0:
                    principal.dir = 7
                else:
                    principal.dir = 3
            else:
                if dy < 0:
                    principal.dir = 0
                elif dy > 0:
                    principal.dir = 1

            # principal.pos.x += dx
            # principal.pos.y += dy

            # If reached the target step, remove it from the path
            if distance < principal.speed * 1.5:
                principal.path.pop(0)
            
        # principal collision
        tl = lvl.coord_to_tile(principal.pos.x, principal.pos.y)
        br = lvl.coord_to_tile(principal.pos.x + principal.pos.width, principal.pos.y + principal.pos.height)

        # loop over all tiles the principal is touching, checking collision with each
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
                    overlap = rect_overlap(principal.pos, tile_rect)

                    # vertical resolution
                    if overlap[0] > overlap[1]:
                        # if principal vertical midpoint is at or above tile vertical midpoint, resolve up
                        if principal.pos.y + (principal.pos.height / 2) <= tile_rect.y + (tile_rect.height / 2):
                            principal.pos.y = tile_rect.y - principal.pos.height
                        # resolve down
                        else:
                            principal.pos.y = tile_rect.y + tile_rect.height
                    # horizontal resolution
                    else:
                        # if principal horizontal midpoint is at or left of tile horizontal midpoint, resolve left
                        if principal.pos.x + (principal.pos.width / 2) <= tile_rect.x + (tile_rect.width / 2):
                            principal.pos.x = tile_rect.x - principal.pos.width
                        # resolve right
                        else:
                            principal.pos.x = tile_rect.x + tile_rect.width

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
            pygame.draw.rect(screen, "green" if not principal.can_see_player else "yellow", pygame.Rect(player.pos.x - camera.x, player.pos.y - camera.y, player.pos.width, player.pos.height))

        # draw principal
        pygame.draw.rect(screen, "red", pygame.Rect(principal.pos.x - camera.x, principal.pos.y - camera.y, principal.pos.width, principal.pos.height))

        # draw principal direction
        dir_mark = pygame.Rect(0, 0, 8, 8)

        dir_mark.x = principal.pos.x + principal.pos.width / 2 - dir_mark.width / 2
        dir_mark.y = principal.pos.y + principal.pos.height / 2 - dir_mark.height / 2

        if principal.dir == 0:
            dir_mark.y -= principal.pos.height
        elif principal.dir == 1:
            dir_mark.y += principal.pos.height
        elif principal.dir == 2:
            dir_mark.x -= principal.pos.width
        elif principal.dir == 3:
            dir_mark.x += principal.pos.width
        elif principal.dir == 4:
            dir_mark.x -= principal.pos.width
            dir_mark.y -= principal.pos.height
        elif principal.dir == 5:
            dir_mark.x += principal.pos.width
            dir_mark.y -= principal.pos.height
        elif principal.dir == 6:
            dir_mark.x -= principal.pos.width
            dir_mark.y += principal.pos.height
        elif principal.dir == 7:
            dir_mark.x += principal.pos.width
            dir_mark.y += principal.pos.height

        pygame.draw.rect(screen, "black", pygame.Rect(dir_mark.x - camera.x, dir_mark.y - camera.y, dir_mark.width, dir_mark.height))

        # draw principal path
        if principal.path and len(principal.path) >= 2:
            pygame.draw.lines(screen, "orange", False, [(pos[0] - camera.x, pos[1] - camera.y) for pos in principal.path])

        # draw principal view angle
        dir_mark_pos = pygame.Vector2(dir_mark.x + dir_mark.width / 2, dir_mark.y + dir_mark.height)
        principal_pos = pygame.Vector2(principal.pos.x + principal.pos.width / 2, principal.pos.y + principal.pos.height / 2)
        
        lp = (principal_pos.x + (dir_mark_pos.x - principal_pos.x) * math.cos(principal.viewing_angle / 2) - (dir_mark_pos.y - principal_pos.y) * math.sin(principal.viewing_angle / 2), principal_pos.y + (dir_mark_pos.x - principal_pos.x) * math.sin(principal.viewing_angle / 2) + (dir_mark_pos.y - principal_pos.y) * math.cos(principal.viewing_angle / 2))
        rp = (principal_pos.x + (dir_mark_pos.x - principal_pos.x) * math.cos(-principal.viewing_angle / 2) - (dir_mark_pos.y - principal_pos.y) * math.sin(-principal.viewing_angle / 2), principal_pos.y + (dir_mark_pos.x - principal_pos.x) * math.sin(-principal.viewing_angle / 2) + (dir_mark_pos.y - principal_pos.y) * math.cos(-principal.viewing_angle / 2))

        pygame.draw.circle(screen, "black", (lp[0] - camera.x, lp[1] - camera.y), 5)
        pygame.draw.circle(screen, "black", (rp[0] - camera.x, rp[1] - camera.y), 5)

        # left ray
        if True:
            dx = lp[0] - principal_pos.x
            dy = lp[1] - principal_pos.y
                        
            dist = math.sqrt(dx**2 + dy**2)
            inc = lvl.tile_size / 2

            ddx = dx / dist * inc
            ddy = dy / dist * inc

            rpos = [principal_pos.x, principal_pos.y]

            while True:
                rpos[0] += ddx
                rpos[1] += ddy

                tile = lvl.coord_to_tile(rpos[0], rpos[1])

                if lvl.tiles[tile[1]][tile[0]].t == 0:
                    break

            pygame.draw.line(screen, "black", (principal_pos.x - camera.x, principal_pos.y - camera.y), (rpos[0] - camera.x, rpos[1] - camera.y))

        # right ray
        if True:
            dx = rp[0] - principal_pos.x
            dy = rp[1] - principal_pos.y
                        
            dist = math.sqrt(dx**2 + dy**2)
            inc = lvl.tile_size / 2

            ddx = dx / dist * inc
            ddy = dy / dist * inc

            rpos = [principal_pos.x, principal_pos.y]

            while True:
                rpos[0] += ddx
                rpos[1] += ddy

                tile = lvl.coord_to_tile(rpos[0], rpos[1])

                if lvl.tiles[tile[1]][tile[0]].t == 0:
                    break

            pygame.draw.line(screen, "black", (principal_pos.x - camera.x, principal_pos.y - camera.y), (rpos[0] - camera.x, rpos[1] - camera.y))

        # midpoint ray
        if principal.view_midpoint != None:
            pygame.draw.line(screen, "black", (principal_pos.x - camera.x, principal_pos.y - camera.y), (principal.view_midpoint[0] - camera.x, principal.view_midpoint[1] - camera.y))

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
