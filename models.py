from dataclasses import dataclass, field

@dataclass
class Fighter:
    name: str
    max_hp: int
    attack: int
    defense: int
    speed: int
    hp: int = field(default=None)

    def __post_init__(self):
        # Runs after setup of a fighter, sets the HP to the max
        if self.hp is None:
            self.hp = self.max_hp
        elif self.hp > self.max_hp:
            raise ValueError(f"HP cannot exceed Max HP {self.hp}/{self.max_hp}")

    def __str__(self):
        return f"{self.name} | HP: {self.hp}/{self.max_hp}\nAttack: {self.attack} | Defense: {self.defense} | Speed: {self.speed}"

    #This method applies the damage to the fighter, and returns a true if the fighter dies
    def take_damage(self, damage: int) -> bool:
        self.hp = max(0, self.hp - damage)
        return self.hp == 0