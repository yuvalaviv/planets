from dataclasses import dataclass


@dataclass
class AnimalConfig:
    """
    Configuration object to controlling the lifecycle behavior of animal entity
    """
    age_increment: float
    hunger_increment: int
    max_hunger: int
    interval: int
