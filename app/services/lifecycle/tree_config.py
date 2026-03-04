from dataclasses import dataclass


@dataclass
class TreeConfig:
    """
    Configuration object to controlling the lifecycle behavior of tree entity
    """
    height_increment: float
    interval: int
