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

def simulate_fight(fighter1, fighter2, verbose=False):
    #Initialize variables for fight simulator
    death = False
    attack_counter = 0

    while not death:
        attack_counter += 1
        attacking = active_turn(fighter1, fighter2)
        defending = fighter2 if attacking is fighter1 else fighter1
        damage = calculate_damage(attacker=attacking, defender=defending)
        death = defending.take_damage(damage)
        
        if verbose:
            print(f"{attacking.name} attacks {defending.name} for {damage} damage!")
            print(f"{fighter1.name}: {fighter1.hp}/{fighter1.max_hp} | {fighter2.name}: {fighter2.hp}/{fighter2.max_hp}")

        if death:
            if verbose:
                print(f"{defending.name}'s HP has hit 0. {attacking.name} wins!")
            return {
                "winner": attacking.name,
                "hp_remaining": attacking.hp,
                "actions": attack_counter
            }