from math import sqrt
from random import randint

def investigate_sounds(state):
    if detect_sound(state):
        sound_source = state.sound_source 
        move_towards_sound_source(state, sound_source)
        return True
    return False

def detect_sound(state):
    return state.sound_detected

def move_towards_sound_source(state, sound_source):
    if state and sound_source:
        # Update Principal's current target to the sound source
        state.principal.current_target = sound_source
        state.principal.stage = 'chasing'
        return True
    return False


def check_is_player_in_front(state):
    
    # 1. Obtain Rects
    player_rect = state.player.rect
    principal_rect = state.principal.rect
    
    # 2. Determine Facing Direction
    facing_direction = state.principal.facing_direction
    
    # 3. Check Player Position
    if facing_direction == "right":
        return (player_rect.left > principal_rect.right and
                abs(player_rect.centery - principal_rect.centery) <= 32)
    
    elif facing_direction == "left":
        return (player_rect.right < principal_rect.left and
                abs(player_rect.centery - principal_rect.centery) <= 32)
    
    elif facing_direction == "up":
        return (player_rect.bottom < principal_rect.top and
                abs(player_rect.centerx - principal_rect.centerx) <= 32)
    
    elif facing_direction == "down":
        return (player_rect.top > principal_rect.bottom and
                abs(player_rect.centerx - principal_rect.centerx) <= 32)
    
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
    state.principle.target = (x,y) # No attribute called target in Main (talk to team)
    
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
    state.principle.target = player_pos
    
    pass
