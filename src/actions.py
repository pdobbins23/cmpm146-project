import random
import time
import helper_functions

def action_principal_chase_player(state):
    state.principal.target = (state.player.pos.x + state.player.pos.width / 2, state.player.pos.y + state.player.pos.height / 2)
    state.principal.wandering = False
    state.principal.stage = 2

    return True

def action_principal_investigate_sound(state):
    state.principal.target = state.principal.heard_sound
    state.principal.heard_sound = None
    state.principal.wandering = True
    state.principal.stage = 1
    state.principal.patrol_begin_time = time.time()

    return True

def action_principal_wander_to_point(state):
    tl = state.level.coord_to_tile(state.principal.pos.x, state.principal.pos.y)
    br = state.level.coord_to_tile(state.principal.pos.x + state.principal.pos.width, state.principal.pos.y + state.principal.pos.height)

    wander_range = 5

    tlx = tl[0] - wander_range if tl[0] - wander_range > 0 else 1
    tly = tl[1] - wander_range if tl[1] - wander_range > 0 else 1
    brx = br[0] + wander_range if br[0] + wander_range < state.level.width else state.level.width - 1
    bry = br[1] + wander_range if br[1] + wander_range < state.level.height else state.level.height - 1

    random_tile_x = random.randint(tlx, brx)
    random_tile_y = random.randint(tly, bry)

    while state.level.tiles[random_tile_y][random_tile_x].t != 8:
        random_tile_x = random.randint(tlx, brx)
        random_tile_y = random.randint(tly, bry)
    
    # Save point to target
    # random_x = random_tile_x * state.level.tile_size + random.random() * state.level.tile_size
    # random_y = random_tile_y * state.level.tile_size + random.random() * state.level.tile_size
    x = random_tile_x * state.level.tile_size + state.level.tile_size / 2
    y = random_tile_y * state.level.tile_size + state.level.tile_size / 2
    
    state.principal.target = (x, y) # No attribute called target in Main (talk to team)
    
    # print(f"Setting random target: ({x}, {y})")
    
    state.principal.wandering = True

    return True

def action_principal_patrol_last_player_location(state):
    state.principal.target = state.principal.last_seen_player_pos
    state.principal.stage = 1
    state.principal.patrol_begin_time = time.time()
    state.principal.wandering = True

    return True

def action_principal_roam(state):
    state.principal.stage = 0
    state.principal.wandering = False

    return True

def action_principal_search_nearby_locker(state):
    shortest_path = None
    shortest_pos = None
    target_locker = None

    # print("searching for locker")
    
    for i, locker in enumerate(state.lockers):
        locker_tile = state.level.coord_to_tile(locker.pos.x, locker.pos.y)
        path = helper_functions.a_star(state.level, (state.principal.pos.x, state.principal.pos.y), (locker_tile[0] * state.level.tile_size, locker_tile[1] * state.level.tile_size))

        if path == None:
            continue

        if shortest_path == None or len(path) < len(shortest_path):
            shortest_path = path
            shortest_pos = (locker.pos.x, locker.pos.y)
            target_locker = i

    # too far
    if target_locker == None or len(shortest_path) > 20:
        return False

    # print("searching nearby locker")

    state.principal.target_locker = target_locker
    state.principal.target = shortest_pos
    state.principal.wandering = True
    
    return True
