import copy
from engine import simulate_fight
from models import Fighter

def run_simulation(fighter1_template: Fighter, fighter2_template: Fighter, num_runs: int):
    results = []

    for _ in range(num_runs):
        fighter1 = copy.deepcopy(fighter1_template)
        fighter2 = copy.deepcopy(fighter2_template)

        result = simulate_fight(fighter1=fighter1, fighter2=fighter2, verbose=False)

        results.append(result)

    return results