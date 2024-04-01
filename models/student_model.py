from pydantic import BaseModel
from typing import List


# defines a Pydantic model Student with four fields
class Student(BaseModel):
    name: str
    id: int
    age: int
    classes: List[str]
