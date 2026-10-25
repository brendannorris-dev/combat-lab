from models import Fighter
from constants import TURN_THRESHOLD
import random

def calculate_damage(attacker: Fighter, defender: Fighter) -> int:
    #Ensures that a fighter always deals a minimum of one damage
    damage = max(1, attacker.attack - defender.defense)
    return damage

def active_turn(fighter1: Fighter, fighter2: Fighter) -> Fighter:
    #New version of active turn utilizes a global time tracking threshold (100), not relative speeds
    #Checks for both fighters above the threshold and breaks the tie
    if fighter1.turn_meter >= TURN_THRESHOLD and fighter2.turn_meter >= TURN_THRESHOLD:
        if fighter1.turn_meter > fighter2.turn_meter:
            fighter1.turn_meter -= TURN_THRESHOLD
            return fighter1
        elif fighter2.turn_meter > fighter1.turn_meter:
            fighter2.turn_meter -= TURN_THRESHOLD
            return fighter2
        else:
            result = random.choice((fighter1, fighter2))
            result.turn_meter -= TURN_THRESHOLD
            return result
    #Otherwise checks each individually and returns; otherwise returns none and no attacks for that tick
    else:
        if fighter1.turn_meter >= TURN_THRESHOLD:
            fighter1.turn_meter -= TURN_THRESHOLD
            return fighter1
        if fighter2.turn_meter >= TURN_THRESHOLD:
            fighter2.turn_meter -= TURN_THRESHOLD
            return fighter2
    return None
        

def simulate_fight(fighter1, fighter2, verbose=False):
    #Initialize variables for fight simulator
    death = False
    attack_counter = 0
    ticks_elapsed = 0

    while not death:
        #Moves forward one tick, fighters move in timeline equal to their speed
        ticks_elapsed += 1
        fighter1.advance_turn()
        fighter2.advance_turn()

        #Creating an inner loop to account for when a fighter hits the turn threshold more than once or both fighters hit the threshold without progressing ticks
        while True:
            #Sets attacker to who is returned from active_turn function, exits if None is returned
            attacking = active_turn(fighter1, fighter2)
            if attacking is None:
                break
            defending = fighter2 if attacking is fighter1 else fighter1

            #Registers an attack happens, raising the counter if so
            attack_counter += 1
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
                    "actions": attack_counter,
                    "ticks_elapsed": ticks_elapsed
                }