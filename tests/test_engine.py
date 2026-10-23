import unittest
from models import Fighter
from engine import calculate_damage

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