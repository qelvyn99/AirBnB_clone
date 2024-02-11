#!/usr/bin/python3

"""Review Module:
Inherits from Superclass BaseModel
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """Review class that inherits from BaseModel."""
    place_id: str = ""
    user_id: str = ""
    text: str = ""
