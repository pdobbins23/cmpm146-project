import math
from queue import PriorityQueue

# new a_star
def calc_point_location(start_tile, start_pos, end_tile):
    pass

def heuristic(goal_pos, next_pos):
    return math.sqrt((goal_pos[0] - next_pos[0]) ** 2 + (goal_pos[1] - next_pos[1]) ** 2)

def a_star(level, start_pos, goal_pos):
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

    # skip the current tile
    del path[0]

    return path
