import unittest
from models import Fighter
from engine import calculate_damage, active_turn, simulate_fight

class TestDamage(unittest.TestCase):
    # Test to make sure damage calculation works under normal circumstances
    def test_damage_calculation(self):
        warrior = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=25)
        goblin = Fighter(name="Goblin", max_hp=100, attack=50, defense=25, speed=25)
        result = calculate_damage(warrior, goblin)
        self.assertEqual(result, 25)

    # Test to make sure that it defaults to 1 damage if defender defense is too high
    def test_damage_not_negative(self):
        warrior = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=25)
        wall = Fighter(name="Wall", max_hp=1000, attack=0, defense=500, speed=0)
        result = calculate_damage(warrior, wall)
        self.assertEqual(result, 1)

class TestTurnOrder(unittest.TestCase):
    #Single unit test to ensure the faster fighter moves first
    def test_faster_fighter_active(self):
        warrior = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=25)
        speedy = Fighter(name="Speedy Warrior", max_hp=100, attack=10, defense=10, speed=70)
        moves = active_turn(warrior, speedy)
        self.assertEqual(moves, speedy)
    
    #Multiple call test to ensure that in the event of a turn meter tie, the base faster fighter moves
    def test_tied_at_turn_base_speed_tiebreak(self):
        warrior = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=25)
        doublefast = Fighter(name="Warrior, doubly fast", max_hp=100, attack=50, defense=50, speed=50)
        move1 = active_turn(warrior, doublefast)
        move2 = active_turn(warrior, doublefast)
        self.assertEqual(move1, doublefast)
        self.assertEqual(move2, doublefast)
        move3 = active_turn(warrior, doublefast)
        self.assertEqual(move3, warrior)
    
    #Multiple call test to ensure that slower fighter eventually catches up
    def test_slower_speed_overtakes_turn(self):
        slow = Fighter(name="Slow Fighter", max_hp=100, attack=50, defense=50, speed=15)
        fast = Fighter(name="Fast Fighter", max_hp=100, attack=50, defense=50, speed=50)
        active_turn(slow, fast)
        active_turn(slow, fast)
        active_turn(slow, fast)
        move4 = active_turn(slow, fast)
        self.assertEqual(move4, slow)

    #Call to handle/verify randomness in the event that turn meter and speed tie
    def test_randomness_distribution_in_both_tie(self):
        fighter1 = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=20)
        fighter2 = Fighter(name="Identical Warrior", max_hp=100, attack=50, defense=50, speed=20)

        results = [active_turn(fighter1,fighter2) for _ in range(1000)]
        fighter1_wins = results.count(fighter1)

        #Checks for roughly 50% tiebreak for fighter1
        self.assertTrue(350 < fighter1_wins < 650)

class TestSimulateFight(unittest.TestCase):
    #Test when there is a clear winner and assure they win
    def test_clear_winner(self):
        strong = Fighter(name="Strong Fighter", max_hp=100, attack=20, defense=10, speed=50)
        weak = Fighter(name="Weak Fighter", max_hp=20, attack=5, defense=10, speed=10)
        result = simulate_fight(fighter1=strong,fighter2=weak)
        self.assertEqual(result["winner"], strong.name)

    #Make sure the output of the return case is correct
    def test_return_output_syntax(self):
        strong = Fighter(name="Strong Fighter", max_hp=100, attack=20, defense=10, speed=50)
        weak = Fighter(name="Weak Fighter", max_hp=20, attack=5, defense=10, speed=10)
        result = simulate_fight(fighter1=strong,fighter2=weak)
        self.assertIn("winner", result)
        self.assertIn("hp_remaining", result)
        self.assertIn("actions", result)

    #Assure fight terminates when attacks are minimized to one
    def test_tanky_fighters_still_die(self):
        weak = Fighter(name="Weak Fighter", max_hp=20, attack=5, defense=10, speed=10)
        wall = Fighter(name="Weakened Wall", max_hp=5, attack=0, defense=100, speed=0)
        result = simulate_fight(fighter1=weak, fighter2=wall)
        self.assertEqual(result["winner"], weak.name)

    #Assure symmetrical returns when function is called in reverse (base case before damage complexity)
    def test_reverse_function_returns_same(self):
        strong = Fighter(name="Strong Fighter", max_hp=100, attack=20, defense=10, speed=50)
        weak = Fighter(name="Weak Fighter", max_hp=1, attack=5, defense=10, speed=10)
        result = simulate_fight(fighter1=strong, fighter2=weak)
        strong2 = Fighter(name="Strong Fighter", max_hp=100, attack=20, defense=10, speed=50)
        weak2 = Fighter(name="Weak Fighter", max_hp=1, attack=5, defense=10, speed=10)
        result2 = simulate_fight(fighter1=weak2, fighter2=strong2)
        self.assertEqual(result, result2)

    #Check that the verbose flag does not change the behavior of the function
    def test_verbose_does_not_affect_function(self):
        strong = Fighter(name="Strong Fighter", max_hp=100, attack=20, defense=10, speed=50)
        weak = Fighter(name="Weak Fighter", max_hp=1, attack=5, defense=10, speed=10)
        result = simulate_fight(fighter1=strong, fighter2=weak,verbose=True)
        strong2 = Fighter(name="Strong Fighter", max_hp=100, attack=20, defense=10, speed=50)
        weak2 = Fighter(name="Weak Fighter", max_hp=1, attack=5, defense=10, speed=10)
        result2 = simulate_fight(fighter1=weak2, fighter2=strong2)
        self.assertEqual(result, result2)

    #Low HP results in quick combat
    def test_low_hp_ends_combat_quickly(self):
        strong = Fighter(name="Strong Fighter", max_hp=100, attack=20, defense=10, speed=50)
        weak = Fighter(name="Weak Fighter", max_hp=1, attack=5, defense=10, speed=10)
        result = simulate_fight(fighter1=strong,fighter2=weak)
        self.assertEqual(result["actions"], 1)
        self.assertEqual(result["winner"],strong.name)