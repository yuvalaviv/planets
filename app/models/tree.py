# app/domain/entities/tree.py
from typing import Literal
from .base_entity import EntityBase
import asyncio


class Tree(EntityBase):
    type: Literal["Tree"]
    height: int = 0

    async def process(self):
        while True:
            self.hight += 1
            print(f"Tree {self.ID} grew to {self.hight}")
            await asyncio.sleep(5)
