# For now, you can make up pseudocode state values in the provided state variable for
# the behavior tree nodes, like I did below with "state.is_roaming"
# As this actual state isn't implemented yet
# Whatever values you might need and make up, we will try to provide them from the game model

from nodes import *
from random import randint
def check_is_roaming(state):
    return state.is_roaming

def check_is_patrolling(state):
    return state.is_patrolling

def check_is_chasing(state):
    return state.is_chasing

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
        
def patrol_area(state):
    """
    Maybe add points the principle will follow
    Or 
    just have it throughly check the room its in
    (if features such as hiding in lockers is viable then
    Patrol will open one random)
    """
    pass

def chase_player(state):

    # Get player's x, y coordinates
    player_pos = (state.player.pos.x, state.player.pos.y)
    
    # Set player's position as the Principal's target
    state.principle.target = player_pos
    
    return True
    
def chase_player(state):
    # Set player's position as the Principal's target
    player_pos = (state.player.pos.x, state.player.pos.y)
    state.principle.target = player_pos
    
    return True

def create_behavior_tree():
    root = Selector(name="Principle Behaviors")

    # ROAM STAGE

    roam_stage = Sequence(name="Principle Roaming Stage")
    # only run this behavior if the state says Principle is currently roaming
    check_roam_status = Check(check_is_roaming)
    # TODO: Add roam behaviors to this branch
    roam_stage.child_nodes = [check_roam_status]

    # PATROL STAGE

    patrol_stage = Sequence(name="Principle Patrol Stage")
    # only run this behavior if the state says Principle is currently patrolling
    check_patrol_status = Check(check_is_patrolling)
    # TODO: Add patrol behaviors to this branch
    patrol_stage.child_nodes = [check_patrol_status]

    # CHASE STAGE

    chase_stage = Sequence(name="Principle Chase Stage")
    # only run this behavior if the state says Principle is currently chasing
    check_chase_status = Check(check_is_chasing)
    # TODO: Add chase behaviors to this branch
    chase_stage.child_nodes = [check_chase_status]

    # NOTE: This shouldn't need to be modified
    root.child_nodes = [roam_stage, patrol_stage, chase_stage]

    return root
