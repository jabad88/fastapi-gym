from pydantic import BaseModel


class PostExercise(BaseModel):
    name: str
    reps: int

    class Config:
        orm_mode = True