# app/models/entity.py
from pydantic import BaseModel
from typing import Union, Literal
from datetime import datetime


class EntityBase(BaseModel):
    _id: str
    planet_id: str
    created_at: datetime
    type: str


class Tree(EntityBase):
    type: Literal["Tree"]
    hight: int


class Animal(EntityBase):
    type: Literal["Animal"]
    age: float
    breeding_chance: int


# 👇 This is the magic
Entity = Union[Tree, Animal]
