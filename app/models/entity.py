# app/models/entity.py
from pydantic import BaseModel
from typing import Union, Literal
from datetime import datetime
from random import randint


class EntityBase(BaseModel):
    _id: str
    planet_id: str
    created_at: datetime
    type: str


class Tree(EntityBase):
    type: Literal["Tree"]
    hight: int

    def grow(self):
        self.hight += 1

    def get_height(self):
        return self.hight


class Animal(EntityBase):
    type: Literal["Animal"]
    age: float
    breeding_chance: int

    def grow_older(self, years: float = 1.0):
        self.age += years

    def try_breed(self) -> bool:
        roll = randint(0, 100)
        return roll <= self.breeding_chance

    def get_age(self):
        return self.age


# 👇 This is the magic
Entity = Union[Tree, Animal]
