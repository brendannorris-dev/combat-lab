from dataclasses import dataclass, field
from constants import CRIT_DAMAGE, CRIT_RATE, EVASION_RATE

@dataclass
class Fighter:
    name: str
    max_hp: int
    attack: int
    defense: int
    speed: int
    hp: int = field(default=None)
    turn_meter: int = field(default=None, init=False)
    crit_chance: float = field(default=CRIT_RATE)
    crit_damage_mod: float = field(default=CRIT_DAMAGE)
    evasion_chance: float = field(default=EVASION_RATE)

    def __post_init__(self):
        # Runs after setup of a fighter, sets the HP to the max. Rasies an error if fighter is set up with too much HP
        if self.hp is None:
            self.hp = self.max_hp
        elif self.hp > self.max_hp:
            raise ValueError(f"HP cannot exceed Max HP {self.hp}/{self.max_hp}")

        # Initializes the turn meter at the fighter's speed
        if self.turn_meter is None:
            self.turn_meter = 0

    def __str__(self):
        return f"{self.name} | HP: {self.hp}/{self.max_hp}\nAttack: {self.attack} | Defense: {self.defense} | Speed: {self.speed}"

    #This method applies the damage to the fighter, and returns a true if the fighter dies
    def take_damage(self, damage: int) -> bool:
        self.hp = max(0, self.hp - damage)
        return self.hp == 0

    #This method advances the fighter's turn meter to compare during the simulation
    def advance_turn(self):
        self.turn_meter = self.turn_meter + self.speed