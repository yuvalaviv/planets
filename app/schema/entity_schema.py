# app/schemas/entity_schema.py
from typing_extensions import Annotated
from typing import Union
from pydantic import Field

from app.models.tree import Tree
from app.models.animal import Animal

EntityResponse = Annotated[
    Union[Tree, Animal],
    Field(discriminator="type")
]