import unittest
from models import Fighter
from engine import calculate_damage, active_turn

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