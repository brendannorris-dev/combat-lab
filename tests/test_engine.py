import unittest, random
from models import Fighter
from engine import calculate_damage, active_turn, simulate_fight

class TestDamage(unittest.TestCase):
    # Test to make sure damage calculation works under normal circumstances
    def test_damage_calculation(self):
        random.seed(13)
        warrior = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=25, crit_chance=0)
        goblin = Fighter(name="Goblin", max_hp=100, attack=50, defense=25, speed=25, crit_chance=0, evasion_chance=0, block_chance=0)
        result, _, _, _ = calculate_damage(warrior, goblin)
        self.assertTrue(22 <= result <= 27)

    # Test to make sure that it defaults to 1 damage if defender defense is too high
    def test_damage_not_negative(self):
        random.seed(13)
        warrior = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=25, crit_chance=0)
        wall = Fighter(name="Wall", max_hp=1000, attack=0, defense=500, speed=0, evasion_chance=0, block_chance=0)
        result, _, _, _ = calculate_damage(warrior, wall)
        self.assertEqual(result, 1)

    # Test to assure critical hit applies appropriate damage calculation
    def test_guaranteed_crit_changes_damage(self):
        warrior = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=100, crit_chance=1)
        dummy = Fighter(name="Dummy", max_hp=1000, attack=0, defense=0, speed=0, evasion_chance=0, block_chance=0)
        result, _, _, _ = calculate_damage(warrior, dummy)
        self.assertTrue(result > 50)

    # Test to assure random distribution of critical hits (when crit chance is boosted to 50%)
    def test_randomness_distribution_crit_hit(self):
        results = []
        warrior = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=100, crit_chance=0.5)
        dummy = Fighter(name="Dummy", max_hp=1000, attack=0, defense=0, speed=0, evasion_chance=0, block_chance=0)

        for _ in range(1000):
            _, crit, _, _ = calculate_damage(warrior, dummy)
            results.append(crit)

        crit_count = results.count(True)
        self.assertTrue(300 < crit_count < 700)

    #Test guaranteed crit + damage variance is within natural range
    def test_guaranteed_crit_natural_range(self):
        warrior = Fighter(name="Warrior", max_hp=100, attack=10, defense=50, speed=100, crit_chance=1)
        dummy = Fighter(name="Dummy", max_hp=1000, attack=0, defense=0, speed=0, evasion_chance=0, block_chance=0)
        result,_,_,_ = calculate_damage(warrior,dummy)
        self.assertGreaterEqual(result,13)
        self.assertLessEqual(result,16)

    #Test that evasion works
    def test_evasion(self):
        warrior = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=100, evasion_chance=0)
        ghost = Fighter(name="Ghost", max_hp=5, attack = 0, defense = 0, speed=0, evasion_chance=1, block_chance=0)
        result, _, _, _ = calculate_damage(warrior, ghost)
        self.assertEqual(result, 0)

    #Test random distribution of evasion (when evasion is boosted to 50%)
    def test_randomness_distribution_evasion_hit(self):
        results=[]
        warrior = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=100)
        evade_warrior = Fighter(name="Sometimes Evades", max_hp=500, attack=50, defense=50, speed=100, evasion_chance=.5, block_chance=0)

        for _ in range(1000):
            _, _, evade, _ = calculate_damage(warrior,evade_warrior)
            results.append(evade)

        evade_count = results.count(True)
        self.assertTrue(300<evade_count<700)

    #Test that blocked damage occurs
    def test_blocking_works(self):
        warrior = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=100)
        blocker = Fighter(name="Blocker", max_hp=100, attack=50, defense=50, speed=0, block_chance=1)
        _,_,_,blocked = calculate_damage(warrior,blocker)
        self.assertTrue(blocked)

    #Test that blocked damage is reduced 25% of the base damage (accounting for variance)
    def test_blocking_damage_reduction_range(self):
        warrior = Fighter(name="Warrior", max_hp=100, attack=10, defense=50, speed=100, crit_chance=0)
        blocker = Fighter(name="Blocker", max_hp=100, attack=0, defense=0, speed=0, block_chance=1)
        result,_,_,_ = calculate_damage(warrior,blocker)
        self.assertTrue(6 <= result <= 8)

    #Test random distribution of blocked (when block rate is boosted to 50%)
    def test_randomness_distribution_block(self):
        results=[]
        warrior = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=100)
        blocker = Fighter(name="Sometimes Evades", max_hp=500, attack=50, defense=50, speed=100, evasion_chance=0, block_chance=0.5)
        
        for _ in range(1000):
            _, _, _, blocks = calculate_damage(warrior,blocker)
            results.append(blocks)
        
        block_count = results.count(True)
        self.assertTrue(300<block_count<700)


class TestTurnOrder(unittest.TestCase):
    #Single unit test to ensure the faster fighter moves first
    def test_faster_fighter_active(self):
        warrior = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=25, evasion_chance=0, block_chance=0)
        speedy = Fighter(name="Speedy Warrior", max_hp=100, attack=10, defense=10, speed=100, evasion_chance=0, block_chance=0)
        warrior.advance_turn()
        speedy.advance_turn()
        moves = active_turn(warrior, speedy)
        self.assertEqual(moves, speedy)
    
    #Multiple call test to ensure that in the event of a turn meter tie, we use a random choice to break
    def test_tied_at_turn_base_speed_tiebreak(self):
        random.seed(13)
        warrior = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=25, evasion_chance=0, block_chance=0)
        doublefast = Fighter(name="Warrior, doubly fast", max_hp=100, attack=50, defense=50, speed=50, evasion_chance=0, block_chance=0)
        warrior.advance_turn()
        doublefast.advance_turn()
        warrior.advance_turn()
        doublefast.advance_turn()
        move1 = active_turn(warrior, doublefast)
        warrior.advance_turn()
        doublefast.advance_turn()
        warrior.advance_turn()
        doublefast.advance_turn()
        move2 = active_turn(warrior, doublefast)
        self.assertEqual(move1, doublefast)
        self.assertEqual(move2, doublefast)
        move3 = active_turn(warrior, doublefast)
        self.assertEqual(move3, warrior)
    
    #Multiple call test to ensure that slower fighter eventually catches up
    def test_slower_speed_overtakes_turn(self):
        slow = Fighter(name="Slow Fighter", max_hp=100, attack=50, defense=50, speed=15, evasion_chance=0, block_chance=0)
        fast = Fighter(name="Fast Fighter", max_hp=100, attack=50, defense=50, speed=50, evasion_chance=0, block_chance=0)
        slow.advance_turn()
        fast.advance_turn()
        slow.advance_turn()
        fast.advance_turn()
        active_turn(slow, fast)
        slow.advance_turn()
        fast.advance_turn()
        slow.advance_turn()
        fast.advance_turn()
        active_turn(slow, fast)
        slow.advance_turn()
        fast.advance_turn()
        slow.advance_turn()
        fast.advance_turn()
        active_turn(slow, fast)
        slow.advance_turn()
        fast.advance_turn()
        move4 = active_turn(slow, fast)
        self.assertEqual(move4, slow)

    #Test that if two fighters both hit the turn threshold that the one further ahead the threshold acts first
    def test_both_fighters_above_threshold(self):
        fighter1 = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=150, evasion_chance=0, block_chance=0)
        fighter2 = Fighter(name="Warrior 2", max_hp=100, attack=50, defense=50, speed=140, evasion_chance=0, block_chance=0)
        fighter1.advance_turn()
        fighter2.advance_turn()
        winner = active_turn(fighter1=fighter1, fighter2=fighter2)
        self.assertEqual(fighter1, winner)

    #Call to handle/verify randomness in the event that turn meter and speed tie
    def test_randomness_distribution_in_both_tie(self):
        results = []
        for _ in range(1000):
            fighter1 = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=100, evasion_chance=0, block_chance=0)
            fighter2 = Fighter(name="Identical Warrior", max_hp=100, attack=50, defense=50, speed=100, evasion_chance=0, block_chance=0)
            fighter1.advance_turn()
            fighter2.advance_turn()
            winner = active_turn(fighter1=fighter1, fighter2=fighter2)
            results.append(winner.name)

        fighter1_wins = results.count("Warrior")

        #Checks for roughly 50% tiebreak for fighter1
        self.assertTrue(400 < fighter1_wins < 600)

class TestSimulateFight(unittest.TestCase):
    #Test when there is a clear winner and assure they win
    def test_clear_winner(self):
        strong = Fighter(name="Strong Fighter", max_hp=100, attack=20, defense=10, speed=50, evasion_chance=0, block_chance=0)
        weak = Fighter(name="Weak Fighter", max_hp=20, attack=5, defense=10, speed=10, evasion_chance=0, block_chance=0)
        result = simulate_fight(fighter1=strong,fighter2=weak)
        self.assertEqual(result["winner"], strong.name)

    #Make sure the output of the return case is correct
    def test_return_output_syntax(self):
        strong = Fighter(name="Strong Fighter", max_hp=100, attack=20, defense=10, speed=50, evasion_chance=0, block_chance=0)
        weak = Fighter(name="Weak Fighter", max_hp=20, attack=5, defense=10, speed=10, evasion_chance=0, block_chance=0)
        result = simulate_fight(fighter1=strong,fighter2=weak)
        self.assertIn("winner", result)
        self.assertIn("hp_remaining", result)
        self.assertIn("actions", result)

    #Assure fight terminates when attacks are minimized to one
    def test_tanky_fighters_still_die(self):
        weak = Fighter(name="Weak Fighter", max_hp=20, attack=5, defense=10, speed=10, evasion_chance=0, block_chance=0)
        wall = Fighter(name="Weakened Wall", max_hp=5, attack=0, defense=100, speed=0, evasion_chance=0, block_chance=0)
        result = simulate_fight(fighter1=weak, fighter2=wall)
        self.assertEqual(result["winner"], weak.name)

    #Assure symmetrical returns when function is called in reverse (base case before damage complexity)
    def test_reverse_function_returns_same(self):
        strong = Fighter(name="Strong Fighter", max_hp=100, attack=20, defense=10, speed=50, evasion_chance=0, block_chance=0)
        weak = Fighter(name="Weak Fighter", max_hp=1, attack=5, defense=10, speed=10, evasion_chance=0, block_chance=0)
        result = simulate_fight(fighter1=strong, fighter2=weak)
        strong2 = Fighter(name="Strong Fighter", max_hp=100, attack=20, defense=10, speed=50, evasion_chance=0, block_chance=0)
        weak2 = Fighter(name="Weak Fighter", max_hp=1, attack=5, defense=10, speed=10, evasion_chance=0, block_chance=0)
        result2 = simulate_fight(fighter1=weak2, fighter2=strong2)
        self.assertEqual(result, result2)

    #Check that the verbose flag does not change the behavior of the function
    def test_verbose_does_not_affect_function(self):
        strong = Fighter(name="Strong Fighter", max_hp=100, attack=20, defense=10, speed=50, evasion_chance=0, block_chance=0)
        weak = Fighter(name="Weak Fighter", max_hp=1, attack=5, defense=10, speed=10, evasion_chance=0, block_chance=0)
        result = simulate_fight(fighter1=strong, fighter2=weak,verbose=True)
        strong2 = Fighter(name="Strong Fighter", max_hp=100, attack=20, defense=10, speed=50, evasion_chance=0, block_chance=0)
        weak2 = Fighter(name="Weak Fighter", max_hp=1, attack=5, defense=10, speed=10, evasion_chance=0, block_chance=0)
        result2 = simulate_fight(fighter1=weak2, fighter2=strong2)
        self.assertEqual(result, result2)

    #Low HP results in quick combat
    def test_low_hp_ends_combat_quickly(self):
        strong = Fighter(name="Strong Fighter", max_hp=100, attack=20, defense=10, speed=50, evasion_chance=0, block_chance=0)
        weak = Fighter(name="Weak Fighter", max_hp=1, attack=5, defense=10, speed=10, evasion_chance=0, block_chance=0)
        result = simulate_fight(fighter1=strong,fighter2=weak)
        self.assertEqual(result["actions"], 1)
        self.assertEqual(result["winner"],strong.name)