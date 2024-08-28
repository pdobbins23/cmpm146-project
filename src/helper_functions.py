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
    
    # Define window size
    window_width = 1280
    window_height = 720 
    
    # Generate random point
    x = randint(0, window_width)
    y = randint(0, window_height)
    
    # Save point to target
    state.principal.target = (x,y) # No attribute called target in Main (talk to team)
    
    print(f"Setting random target: ({x}, {y})")

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
    
    pass

# code taken and revised from p1
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(node, world):
    neighbors = []
    x, y = node
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(world) and 0 <= ny < len(world[0]) and world[nx][ny].t == 1:
            neighbors.append((nx, ny))

    return neighbors

def reconstruct_path(forward_came_from, backward_came_from, meeting_point):
    path_forward = []
    current = meeting_point
    while current in forward_came_from:
        path_forward.append(current)
        current = forward_came_from[current]
    path_forward.reverse()

    path_backward = []
    current = meeting_point
    while current in backward_came_from:
        path_backward.append(current)
        current = backward_came_from[current]

    return path_forward + path_backward[1:]

def a_star(start, goal, world):
    priority_queue = []
    heappush(priority_queue, (0, start, 'forward'))
    heappush(priority_queue, (0, goal, 'backward'))

    visited_forward = {}
    visited_backward = {}

    cost_to_child_forward = defaultdict(lambda: float('inf'))
    cost_to_child_backward = defaultdict(lambda: float('inf'))

    visited_forward[start] = None
    visited_backward[goal] = None

    cost_to_child_forward[start] = 0
    cost_to_child_backward[goal] = 0

    meeting_point = None

    while priority_queue:
        _, current_node, direction = heappop(priority_queue)

        if direction == 'forward':
            if current_node in visited_backward:
                meeting_point = current_node
                break

            for neighbor in get_neighbors(current_node, world):
                new_cost = cost_to_child_forward[current_node] + 1
                if new_cost < cost_to_child_forward[neighbor]:
                    cost_to_child_forward[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, goal)
                    heappush(priority_queue, (priority, neighbor, 'forward'))
                    visited_forward[neighbor] = current_node

        else:
            if current_node in visited_forward:
                meeting_point = current_node
                break

            for neighbor in get_neighbors(current_node, world):
                new_cost = cost_to_child_backward[current_node] + 1
                if new_cost < cost_to_child_backward[neighbor]:
                    cost_to_child_backward[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, start)
                    heappush(priority_queue, (priority, neighbor, 'backward'))
                    visited_backward[neighbor] = current_node

    if meeting_point is not None:
        return reconstruct_path(visited_forward, visited_backward, meeting_point)

    return None



iii
