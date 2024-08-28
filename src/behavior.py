# For now, you can make up pseudocode state values in the provided state variable for
# the behavior tree nodes, like I did below with "state.is_roaming"
# As this actual state isn't implemented yet
# Whatever values you might need and make up, we will try to provide them from the game model

from nodes import *
from random import randint
from math import sqrt
from helper_functions import check_is_player_in_front, chase_player, detect_sound, move_points_of_interest


def check_is_roaming(state):
    return state.principle.stage == 0

def check_is_patrolling(state):
    return state.principle.stage == 1

def check_is_chasing(state):
    return state.principle.stage == 2
        
def patrol_area(state):
    """
    Maybe add points the principle will follow
    Or 
    just have it throughly check the room its in
    (if features such as hiding in lockers is viable then
    Patrol will open one random)
    """
    pass
    

def create_behavior_tree():
    root = Selector(name="Principle Behaviors")

    # ROAM STAGE

    roam_stage = Sequence(name="Principal Roaming Stage")
    
    # Only run this behavior if the state says Principal is currently roaming
    check_roam_status = Check(check_is_roaming)
    
    # Behaviors for roaming
    prioritize_sight = Selector(name="Prioritize Sight")
    
    # Sight-related behavior
    see_student = Check(check_is_player_in_front)
    chase_player = Action(chase_player)
    sight_behaviors = Sequence(name="Sight Behaviors")
    sight_behaviors.child_nodes = [see_student, chase_player]
    
    # Sound-related behavior
    investigate_sounds = Sequence(name="Investigate Sounds")
    check_for_sound = Check(detect_sound)
    move_towards_sound = Action(investigate_sounds)
    investigate_sounds.child_nodes = [check_for_sound, move_towards_sound]

    # Wander to Points of Interest
    wander_to_points = Sequence(name="Wander to Points of Interest")
    select_point = Action(move_points_of_interest)
    wander_to_points.child_nodes = [select_point]
    
    # Prioritize sight over sound
    prioritize_sight.child_nodes = [sight_behaviors, investigate_sounds]
    
    # Combine all roam behaviors
    roam_stage.child_nodes = [check_roam_status, prioritize_sight, wander_to_points]
    
    # Add roam_stage to the root behavior tree
    root.child_nodes = [roam_stage]

    # PATROL STAGE

    patrol_stage = Sequence(name="Principle Patrol Stage")
    # only run this behavior if the state says Principle is currently patrolling
    check_patrol_status = Check(check_is_patrolling)
    # TODO: Add patrol behaviors to this branch
    patrol_stage.child_nodes = [check_patrol_status]

    # CHASE STAGE

    # CHASE STAGE
    chase_stage = Sequence(name="Principal Chase Stage")
    check_chase_status = Check(check_is_chasing)
    
    # Chase behavior
    chase_player = Action(chase_player)
    chase_stage.child_nodes = [check_chase_status, chase_player]

    # Add stages to the root behavior tree
    root.child_nodes = [roam_stage, patrol_stage, chase_stage]

    return root
