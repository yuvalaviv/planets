import random
from typing import Literal
from .base_entity import EntityBase


class Animal(EntityBase):
    """
    Domain model representing an Animal entity.
    """
    type: Literal["Animal"]
    age: float = 0
    breeding_chance: int = 0
    hungry: int = 0

    def grow(self, increment: float) -> bool:
        """
        Increase age.
        Returns True if reproduction event triggered.
        """
        self.age += increment
        return random.random() < self.breeding_chance / 100

    def increase_hunger(self, increment: int, max_hungry: int) -> None:
        """
        Increase hunger up to max limit.
        """
        self.hungry = min(self.hungry + increment, max_hungry)
