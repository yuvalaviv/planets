from dataclasses import dataclass


@dataclass
class AnimalConfig:
    age_increment: float
    hunger_increment: int
    max_hunger: int
    interval: int
