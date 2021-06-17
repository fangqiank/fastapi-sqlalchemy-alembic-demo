import os
from os.path import join, dirname
import uvicorn

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from dotenv import load_dotenv
import motor.motor_asyncio

from db import python_models

app = FastAPI()

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGODB_URL"))
db = client.college

@app.post("/", response_description="Add new student", response_model=python_models.StudentModel)
async def create_student(student: python_models.StudentModel = Body(...)):
    student = jsonable_encoder(student)
    new_student = await db["students"].insert_one(student)
    created_student = await db["students"].find_one({"_id": new_student.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)

@app.get(
    "/", response_description="List all students", response_model=List[python_models.StudentModel]
)
async def list_students():
    students = await db["students"].find().to_list(1000)
    return students

@app.get(
    "/{id}", response_description="Get a single student", response_model=python_models.StudentModel
)
async def show_student(id: str):
    if (student := await db["students"].find_one({"_id": id})) is not None:
        return student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")

@app.put("/{id}", response_description="Update a student", response_model=python_models.StudentModel)
async def update_student(id: str, student: python_models.UpdateStudentModel = Body(...)):
    student = {k: v for k, v in student.dict().items() if v is not None}

    if len(student) >= 1:
        update_result = await db["students"].update_one({"_id": id}, {"$set": student})

        if update_result.modified_count == 1:
            if (
                updated_student := await db["students"].find_one({"_id": id})
            ) is not None:
                return updated_student

    if (existing_student := await db["students"].find_one({"_id": id})) is not None:
        return existing_student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")

@app.delete("/{id}", response_description="Delete a student",response_model=python_models.StudentModel)
async def delete_student(id: str):
    delete_result = await db["students"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)