from fastapi import FastAPI
from schemas import PostExercise
from models import Exercise
from db import engine, Base, get_db
app = FastAPI()

get_db()

@app.get("/")
async def root():
    return {"message": "Hello World"}



# @app.post("/exercise")
# async def add_exercise(post:PostExercise,db:db_dependency):
#     db.add

#     return {"name":post.name,
#             "reps":post.reps}

Base.metadata.create_all(bind=engine)