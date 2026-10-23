from models import Fighter

def calculate_damage(attacker: Fighter, defender: Fighter) -> int:
    damage = max(1, attacker.attack - defender.defense)
    return damage