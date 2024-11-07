from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import uuid4
from threading import Lock
app = FastAPI()
class Student(BaseModel):
    id: Optional[str] = None  
    name: str  
    age: int  
    email: EmailStr  
students_db = {}
db_lock = Lock()
@app.post("/students", response_model=Student)
def create_student(student: Student):
    with db_lock:
        student_id = str(uuid4())  
        student.id = student_id
        students_db[student_id] = student
        return student


@app.get("/students", response_model=List[Student])
def get_all_students():
    with db_lock:
        return list(students_db.values())
    

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: str):
    with db_lock:
        student = students_db.get(student_id)
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
