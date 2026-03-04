"""
EntityResponse schema definition.

This module defines the polymorphic response model used for entity-related
API endpoints. It leverages Pydantic's discriminated unions to dynamically
select the appropriate domain model based on the `type` field.

Supported entity types:
    - Tree
    - Animal

The `type` field acts as a discriminator, meaning:
    - If `type="Tree"` → the response will be validated as Tree
    - If `type="Animal"` → the response will be validated as Animal
"""

from typing_extensions import Annotated
from typing import Union
from pydantic import Field

from app.models.tree import Tree
from app.models.animal import Animal


EntityResponse = Annotated[
    Union[Tree, Animal],
    Field(discriminator="type")
]