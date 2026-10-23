from models import Fighter
import random

def calculate_damage(attacker: Fighter, defender: Fighter) -> int:
    #Ensures that a fighter always deals a minimum of one damage
    damage = max(1, attacker.attack - defender.defense)
    return damage

def active_turn(fighter1: Fighter, fighter2: Fighter) -> Fighter:
    #Whichever is further ahead in the timeline acts (is returned) and the other has their turn_meter pushed forward
    if fighter1.turn_meter > fighter2.turn_meter:
        fighter2.advance_turn()
        return fighter1
    elif fighter2.turn_meter > fighter1.turn_meter:
        fighter1.advance_turn()
        return fighter2
    #Ties are broken by the fighter's base speed
    else:
        if fighter1.speed > fighter2.speed:
            fighter2.advance_turn()
            return fighter1
        elif fighter2.speed > fighter1.speed:
            fighter1.advance_turn()
            return fighter2
        else:
            result = random.choice((fighter1, fighter2))
            if result == fighter1:
                fighter2.advance_turn()
            else:
                fighter1.advance_turn()
            return result