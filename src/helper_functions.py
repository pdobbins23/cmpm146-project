import behavior
from math import sqrt
from random import randint

def investigate_sounds(state) -> bool:
    if detect_sound(state):
        sound_source = state.sound_source 
        move_towards_sound_source(state, sound_source)
        return True
    return False

def detect_sound(state) -> bool:
    return state.sound_detected

def move_towards_sound_source(state, sound_source):
    # Calculate direction vector to the sound source
    direction_x = sound_source.x - state.principal.rect.centerx
    direction_y = sound_source.y - state.principal.rect.centery
    
    # Normalize the direction
    length = sqrt(direction_x**2 + direction_y**2)
    direction_x /= length
    direction_y /= length
    
    # Move Principal
    state.principal.rect.x += direction_x * state.principal.speed
    state.principal.rect.y += direction_y * state.principal.speed

def check_is_player_in_front(state):
    """
    Explanation:
    1. Obtain Rects: Retrieve the rectangles for the player and the Principal from the game state.
    2. Determine Facing Direction: Get the direction the Principal is facing.
    3. Check Player Position:
    - Facing Right: Player must be to the right of the Principal and within a vertical range of 32 pixels.
    - Facing Left: Player must be to the left of the Principal and within a vertical range of 32 pixels.
    - Facing Up: Player must be above the Principal and within a horizontal range of 32 pixels.
    - Facing Down: Player must be below the Principal and within a horizontal range of 32 pixels.
    4. Default Case: If the facing direction is unknown or not set, return False.
    5. Return Result: Return whether the player is in front of the Principal based on the checks.
    """
    pass

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

def chase_player(state):

    # Get player's x, y coordinates
    player_pos = (state.player.pos.x, state.player.pos.y)
    
    # Set player's position as the Principal's target
    state.principle.target = player_pos
    
    return True