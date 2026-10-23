import unittest
from models import Fighter

class TestFighter(unittest.TestCase):
    #Test that the HP defaults to the Max HP
    def test_hp_initializes_at_max(self):
        attacker = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=25)
        self.assertEqual(attacker.hp, 100)

    #Test that the Take Damage method reduces the HP appropriately
    def test_take_damage_reduces_hp(self):
        attacker = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=25)
        attacker.take_damage(10)
        self.assertEqual(attacker.hp, 90)

    #Test that the Take Damage method returns true if HP hits 0
    def test_died_if_hp_zero(self):
        attacker = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=25)
        died = attacker.take_damage(100)
        self.assertTrue(died)

    #Test to make sure that damage doesn't turn negative
    def test_no_negative_hp(self):
        attacker = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=25)
        attacker.take_damage(150)
        self.assertGreaterEqual(attacker.hp, 0)

    #Test for wounded fighter, manually setting hp during setup
    def test_hp_not_equal_max_hp(self):
        attacker = Fighter(name="Warrior", max_hp=100, attack=50, defense=50, speed=25, hp=50)
        self.assertEqual(attacker.hp, 50)

    #Test for input issue where HP is initially set higher than Max HP
    def test_hp_not_greater_max_hp(self):
        with self.assertRaises(ValueError):
            attacker = Fighter(name="Invalid Warrior", max_hp=100, attack=50, defense=50, speed=25, hp=1000)