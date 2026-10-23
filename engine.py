from models import Fighter

def calculate_damage(attacker: Fighter, defender: Fighter) -> int:
    damage = max(1, attacker.attack - defender.defense)
    return damage

def active_turn(fighter1: Fighter, fighter2: Fighter) -> Fighter:
    if fighter1.turn_meter > fighter2.turn_meter:
        fighter2.advance_turn()
        return fighter1
    elif fighter2.turn_meter > fighter1.turn_meter:
        fighter1.advance_turn()
        return fighter2
    else:
        if fighter1.speed > fighter2.speed:
            fighter2.advance_turn()
            return fighter1
        else:
            fighter1.advance_turn()
            return fighter2