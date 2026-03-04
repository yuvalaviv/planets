# app/domain/entities/tree.py
from typing import Literal
from .base_entity import EntityBase


class Tree(EntityBase):
    """
    Domain model representing a Tree entity.
    """
    type: Literal["Tree"]
    height: int = 0

    def grow(self, increment: float) -> None:
        """
        Increase height.
        """
        self.hight += increment

