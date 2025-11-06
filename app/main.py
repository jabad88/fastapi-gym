from fastapi import FastAPI, Depends
from schemas import PostExercise
from models import Exercise
from db import engine, Base, get_db
from sqlalchemy.orm import Session


app = FastAPI()

Base.metadata.create_all(engine)

get_db()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/exercise")
async def add_exercise(post:PostExercise, db: Session = Depends(get_db)):
    new_exercise = Exercise(name=post.name, reps=post.reps)
    
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)

    return new_exercise
