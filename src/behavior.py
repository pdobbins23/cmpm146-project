# For now, you can make up pseudocode state values in the provided state variable for
# the behavior tree nodes, like I did below with "state.is_roaming"
# As this actual state isn't implemented yet
# Whatever values you might need and make up, we will try to provide them from the game model

from nodes import *
from random import randint
from math import sqrt
from helper_functions import *

def check_is_roaming(state):
    return state.principal.stage == 0

def check_is_patrolling(state):
    return state.principal.stage == 1

def check_is_chasing(state):
    print("CHECKING CHASING")
    return state.principal.stage == 2

def check_is_not_wandering(state):
    return not state.principal.wandering

def patrol_area(state):
    """
    Maybe add points the principle will follow
    Or 
    just have it throughly check the room its in
    (if features such as hiding in lockers is viable then
    Patrol will open one random)
    """
    patrol_points = state.patrol_points  # TBD
    current_point = state.current_patrol_point  # where the principal currently is
    
    # moves to the next patrol point - cycles thru
    next_point = (current_point + 1) % len(patrol_points)
    state.move_to(patrol_points[next_point])
    
    # check lockers and areas randomly
    if randint(0, 100) < 20:  # 20% chance to open a locker
        locker = state.get_random_locker()
        state.search_locker(locker)
    
    # update patrol state
    state.current_patrol_point = next_point

def detect_sound(state):
    return state.principal.heard_sound != None

def check_out_of_sight(state):
    return not state.principal.can_see_player and state.time - state.principal.last_seen_player_time >= 5000

def revert_to_roam(state):
    state.principal.stage = 0

def shift_to_patrol(state):
    state.principal.stage = 1

def last_known_position(state):
    state.principal.target = state.principal.last_seen_player_pos

def create_behavior_tree():
    root = Selector(name="Principle Behaviors")

    # ROAM STAGE

    roam_stage = Sequence(name="Principal Roaming Stage")
    check_roam_status = Check(check_is_roaming)

    prioritize_sight = Selector(name="Prioritize Sight")

    # Sight-related behavior
    sight_behaviors = Sequence(name="Sight Behaviors")
    see_student = Check(check_is_player_in_front)
    chase_student = Action(chase_player)
    sight_behaviors.child_nodes = [see_student, chase_student]

    # Sound-related behavior
    sound_behaviors = Sequence(name="Sound Behaviors")
    check_for_sound = Check(detect_sound)
    move_towards_sound = Action(investigate_sounds)
    sound_behaviors.child_nodes = [check_for_sound, move_towards_sound]

    # Wander to Points of Interest
    wander_to_points = Sequence(name="Wander to Points of Interest")
    check_not_wandering = Check(check_is_not_wandering)
    select_point = Action(move_random_point)
    wander_to_points.child_nodes = [check_not_wandering, select_point]

    # Prioritize sight over sound
    prioritize_sight.child_nodes = [sight_behaviors, sound_behaviors, wander_to_points]

    # Combine all roam behaviors
    roam_stage.child_nodes = [check_roam_status, prioritize_sight]

    # PATROL STAGE

    patrol_stage = Sequence(name="Principle Patrol Stage")
    check_patrol_status = Check(check_is_patrolling)

    patrol_selector = Selector(name="Patrol: Sight and Sound")
    patrol_action = Action(patrol_area)
    patrol_selector.child_nodes = [see_student, check_for_sound, patrol_action] # priority
    patrol_stage.child_nodes = [check_patrol_status, patrol_selector]  

    # CHASE STAGE

    chase_stage = Sequence(name="Principle Chase Stage")
    check_chase_status = Check(check_is_chasing)

    chase_sequence = Sequence(name="Chasing Player")
    chase_player_action = Action(chase_player)
    check_out_of_sight_action = Check(check_out_of_sight)
    stop_chasing = Action(shift_to_patrol)
    move_to_last_seen = Action(last_known_position)

    chase_sequence.child_nodes = [chase_player_action, check_out_of_sight_action, stop_chasing, move_to_last_seen]

    # NOTE: This shouldn't need to be modified
    root.child_nodes = [roam_stage, patrol_stage, chase_stage]

    return root
