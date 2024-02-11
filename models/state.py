#!/usr/bin/python3

"""State Module:
Inherits from Superclass BaseModel
"""

from models.base_model import BaseModel


class State(BaseModel):
    """State class that inherits from BaseModel."""
    name: str = ""
