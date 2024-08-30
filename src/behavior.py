from random import randint
from math import sqrt

from nodes import *
from helper_functions import *
from checks import *
from actions import *

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

def create_behavior_tree():
    root = Selector(name="Principle Behaviors")

    # ROAM STAGE

    roam_stage = Sequence(name="Principal Roaming Stage")
    roaming = Check(check_principal_roaming)

    prioritize_sight = Selector(name="Prioritize Sight")

    # Sight-related behavior
    sight_sequence = Sequence(name="Sight")
    see_player = Check(check_principal_see_player)
    chase_player = Action(action_principal_chase_player)
    sight_sequence.child_nodes = [see_player, chase_player]

    # Sound-related behavior
    sound_sequence = Sequence(name="Sound")
    hear_sound = Check(check_principal_hear_sound)
    investigate_sound = Action(action_principal_investigate_sound)
    sound_sequence.child_nodes = [hear_sound, investigate_sound]

    # Wander to Points of Interest
    wander_sequence = Sequence(name="Wander")
    not_wandering = Check(check_not(check_principal_wandering))
    wander = Action(action_principal_wander_to_point)
    wander_sequence.child_nodes = [not_wandering, wander]

    # Prioritize sight over sound
    prioritize_sight.child_nodes = [sight_sequence, sound_sequence, wander_sequence]

    # Combine all roam behaviors
    roam_stage.child_nodes = [roaming, prioritize_sight]

    # PATROL STAGE

    patrol_stage = Sequence(name="Principle Patrol Stage")
    patrolling = Check(check_principal_patrolling)

    prioritize_sight = Selector(name="Prioritize Sight")

    # Return to roaming
    calming_sequence = Sequence(name="Calm")
    patrol_over = Check(check_principal_patrol_over)
    roam = Action(action_principal_roam)
    calming_sequence.child_nodes = [patrol_over, roam]

    # Sight-related behavior
    sight_sequence = Sequence(name="Sight")
    see_player = Check(check_principal_see_player)
    chase_player = Action(action_principal_chase_player)
    sight_sequence.child_nodes = [see_player, chase_player]

    # Sound-related behavior
    sound_sequence = Sequence(name="Sound")
    hear_sound = Check(check_principal_hear_sound)
    investigate_sound = Action(action_principal_investigate_sound)
    sound_sequence.child_nodes = [hear_sound, investigate_sound]

    # TODO: Integrate random nearby locker checking

    # Wander to Points of Interest
    wander_sequence = Sequence(name="Wander")
    not_wandering = Check(check_not(check_principal_wandering))
    wander = Action(action_principal_wander_to_point)
    wander_sequence.child_nodes = [not_wandering, wander]

    # Prioritize sight over sound
    prioritize_sight.child_nodes = [calming_sequence, sight_sequence, sound_sequence, wander_sequence]
    
    patrol_stage.child_nodes = [patrolling, prioritize_sight]

    # CHASE STAGE

    chase_stage = Sequence(name="Principle Chase Stage")
    chasing = Check(check_principal_chasing)
    chase_player = Action(action_principal_chase_player)
    cant_see_player = Check(check_principal_last_seen_player_time)
    stop_chasing_player = Action(action_principal_patrol_last_player_location)
    chase_stage.child_nodes = [chasing, chase_player, cant_see_player, stop_chasing_player]

    # NOTE: This shouldn't need to be modified
    root.child_nodes = [roam_stage, patrol_stage, chase_stage]

    return root
