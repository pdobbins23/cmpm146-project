from math import sqrt
from random import randint
from heapq import heappop, heappush
from collections import defaultdict

def investigate_sounds(state):
    if state.principal.heard_sound != None:
        move_towards_sound_source(state, state.principal.heard_sound)
        return True
    return False

def move_towards_sound_source(state, sound_source):
    # reset heard_sound
    state.principal.heard_sound = None

    # Update Principal's current target to the sound source
    state.principal.target = sound_source
    state.principal.stage = 2 # chase stage to position

def check_is_player_in_front(state):
    # 1. Obtain Rects
    player_rect = state.player.pos
    principal_rect = state.principal.pos
    
    # 2. Determine Facing Direction
    facing_direction = state.principal.dir
    
    # 3. Check Player Position
    if facing_direction == 3:
        return (player_rect.x > principal_rect.x + principal_rect.width and
                abs((player_rect.y + player_rect.height / 2) - (principal_rect.y + principal_rect.height / 2)) <= 32)
    
    elif facing_direction == 2:
        return (player_rect.x + player_rect.width < principal_rect.x and
                abs((player_rect.y + player_rect.height / 2) - (principal_rect.y + principal_rect.height / 2)) <= 32)
    
    elif facing_direction == 0:
        return (player_rect.y + player_rect.height < principal_rect.y and
                abs((player_rect.x + player_rect.width / 2) - (principal_rect.x + principal_rect.width / 2)) <= 32)
    
    elif facing_direction == 1:
        return (player_rect.y > principal_rect.y + principal_rect.height and
                abs((player_rect.x + player_rect.width / 2) - (principal_rect.x + principal_rect.width / 2)) <= 32)
    
    # 4. Default Case
    return False

def move_random_point(state):
    import random

    state.principal.wandering = True
    
    tl = state.level.coord_to_tile(state.principal.pos.x, state.principal.pos.y)
    br = state.level.coord_to_tile(state.principal.pos.x + state.principal.pos.width, state.principal.pos.y + state.principal.pos.height)

    wander_range = 5

    tlx = tl[0] - wander_range if tl[0] - wander_range > 0 else 1
    tly = tl[1] - wander_range if tl[1] - wander_range > 0 else 1
    brx = br[0] + wander_range if br[0] + wander_range < state.level.width else state.level.width - 1
    bry = br[1] + wander_range if br[1] + wander_range < state.level.height else state.level.height - 1

    random_tile_x = random.randint(tlx, brx)
    random_tile_y = random.randint(tly, bry)

    while state.level.tiles[random_tile_y][random_tile_x].t != 1:
        random_tile_x = random.randint(tlx, brx)
        random_tile_y = random.randint(tly, bry)
    
    # Save point to target
    # random_x = random_tile_x * state.level.tile_size + random.random() * state.level.tile_size
    # random_y = random_tile_y * state.level.tile_size + random.random() * state.level.tile_size
    x = random_tile_x * state.level.tile_size + state.level.tile_size / 2
    y = random_tile_y * state.level.tile_size + state.level.tile_size / 2
    
    state.principal.target = (x, y) # No attribute called target in Main (talk to team)
    
    # print(f"Setting random target: ({x}, {y})")

    # Return success
    return True

def move_points_of_interest(state, points_of_interest):
    if not points_of_interest:
        return False  # No points of interest to move towards

    # Find the closest point of interest
    principal_pos = state.principal.pos
    closest_point = min(points_of_interest, key=lambda p: sqrt((p[0] - principal_pos.x)**2 + (p[1] - principal_pos.y)**2))

    # Set the closest point as the Principal's target
    x, y = closest_point[0]
    state.principal.target.x = x
    state.principal.target.y = y

    return True

def chase_player(state):
    # Get player's x, y coordinates
    player_pos = (state.player.pos.x, state.player.pos.y)
    
    # Set player's position as the Principal's target
    state.principal.target = player_pos

# new a_star
def calc_point_location(start_tile, start_pos, end_tile):
    pass

def heuristic(goal_pos, next_pos):
    return sqrt((goal_pos[0] - next_pos[0]) ** 2 + (goal_pos[1] - next_pos[1]) ** 2)

def a_star(level, start_pos, goal_pos):
    from queue import PriorityQueue

    start_tile = level.coord_to_tile(start_pos[0], start_pos[1])
    goal_tile = level.coord_to_tile(goal_pos[0], goal_pos[1])

    to_visit = PriorityQueue()
    to_visit.put((0, start_tile, start_pos))
    
    came_from = dict()
    cost_so_far = dict()
    
    came_from[start_tile] = None
    cost_so_far[start_tile] = 0

    while not to_visit.empty():
        priority, current, current_pos = to_visit.get()

        if current == goal_tile:
            break

        if current not in level.adj_tiles:
            break

        for next in level.adj_tiles[current]:
            # next_pos = calc_point_location(current, current_pos, next)
            next_pos = (next[0] * level.tile_size + level.tile_size / 2, next[1] * level.tile_size + level.tile_size / 2)
            new_cost = cost_so_far[current] + heuristic(current_pos, next_pos)

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal_pos, next_pos)
                to_visit.put((priority, next, next_pos))
                came_from[next] = current

    if not goal_tile in came_from:
        return None

    path = [goal_pos]
    cur = goal_tile

    while came_from[cur] != None:
        cur = came_from[cur]
        next_pos = (cur[0] * level.tile_size + level.tile_size / 2, cur[1] * level.tile_size + level.tile_size / 2)
        path.insert(0, next_pos)

    del path[0]

    return path
