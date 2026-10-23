import unittest
from models import Fighter

class TestFighter(unittest.TestCase):
    #Test that the HP defaults to the Max HP
    def test_hp_initializes_at_max(self):
        attacker = Fighter("Warrior", 100, 50, 50, 25)
        self.assertEqual(attacker.hp, 100)

    #Test that the Take Damage method reduces the HP appropriately
    def test_take_damage_reduces_hp(self):
        attacker = Fighter("Warrior", 100, 50, 50, 25)
        attacker.take_damage(10)
        self.assertEqual(attacker.hp, 90)

    #Test that the Take Damage method returns true if HP hits 0
    def test_died_if_hp_zero(self):
        attacker = Fighter("Warrior", 100, 50, 50, 25)
        died = attacker.take_damage(100)
        self.assertTrue(died)

    #Test to make sure that damage doesn't turn negative
    def test_no_negative_hp(self):
        attacker = Fighter("Warrior", 100, 50, 50, 25)
        attacker.take_damage(150)
        self.assertGreaterEqual(attacker.hp, 0)