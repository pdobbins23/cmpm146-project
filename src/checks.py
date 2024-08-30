import random

def check_not(check):
    def c(state):
        return not check(state)
    return c

def check_and(check1, check2):
    def c(state):
        return check1(state) and check2(state)
    return c

def check_or(check1, check2):
    def c(state):
        return check1(state) or check2(state)
    return c

def check_principal_roaming(state):
    return state.principal.stage == 0

def check_principal_patrolling(state):
    return state.principal.stage == 1

def check_principal_chasing(state):
    return state.principal.stage == 2

def check_principal_wandering(state):
    return state.principal.wandering

def check_principal_hear_sound(state):
    return state.principal.heard_sound != None

def check_principal_see_player(state):
    return state.principal.can_see_player

def check_principal_last_seen_player_time(state):
    return state.time - state.principal.last_seen_player_time >= 2

def check_principal_patrol_over(state):
    return state.time - state.principal.patrol_begin_time >= 15

def check_principal_decide_check_locker(state):
    # 20% chance
    return random.random() <= 0.2
