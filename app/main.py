from fastapi import FastAPI, Depends
from schemas import PostExercise
from models import Exercise
from db import engine, Base, get_db
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
import boto3
import auth

app = FastAPI()
app.include_router(auth.router)

load_dotenv()

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


@app.post("/upload")
async def upload_membership_info():


    s3_client = boto3.client(
        service_name='s3',
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
    )
    
    response = s3_client.upload_file("/Users/josh/Documents/fastapi-gym/membership_info.txt", os.getenv("AWS_S3_BUCKET_NAME"),"membership_info1.txt")

    print(f'upload_log_to_aws response: {response}')

    return True


