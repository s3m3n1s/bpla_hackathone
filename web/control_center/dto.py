from pydantic import BaseModel
# from typing import


class Coordinate(BaseModel):
    x: float
    y: float

