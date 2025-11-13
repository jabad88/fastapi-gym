from pydantic import BaseModel


class PostExercise(BaseModel):
    name: str
    reps: int

    class Config:
        orm_mode = True


class UserInDB(BaseModel):
    username: str
    hashed_password: str

    class Config:
        orm_mode = True