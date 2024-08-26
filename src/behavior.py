# For now, you can make up pseudocode state values in the provided state variable for
# the behavior tree nodes, like I did below with "state.is_roaming"
# As this actual state isn't implemented yet
# Whatever values you might need and make up, we will try to provide them from the game model

from nodes import *
from random import randint
from math import sqrt

def check_is_roaming(state):
    return state.is_roaming

def check_is_patrolling(state):
    return state.is_patrolling

def check_is_chasing(state):
    return state.is_chasing
        
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
