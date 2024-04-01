from typing import List
from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from read_write_db import read_from_db, write_to_db

# creating fastapi, for using it to define endpoints late
app = FastAPI()


# defines a Pydantic model Student with four fields
class Student(BaseModel):
    name: str
    id: int
    age: int
    classes: List[str]


# get all students
@app.get("/all-students", response_model=List[Student])
def get_all_students():
    """
    return: this endpoint returns all the students in db
    """
    students = read_from_db()
    return students


# get specific student by id
@app.get("/get-student/{student_id}", response_model=Student)
def get_student(student_id: int = Path(..., description="The ID of the student you would like to view")):
    """
    param student_id: by student_id, we can get the student that we want
    return: a student object, else: error message
    """
    students = read_from_db()
    for student in students:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student id not found")


# add student
@app.post("/add-student", response_model=Student)
def add_student(student_id: int, student: Student):
    """
    param student_id: to check if there is an exist student with this id
    param student: a Student object that we want to add to db
    return: a dictionary of student's details(using Student class)
    """
    students = read_from_db()
    students_ids = []
    for stu in students:
        students_ids.append(stu["id"])
    if student_id in students_ids:
        raise HTTPException(status_code=400, detail="Student id is already exists.")
    create_student = {"name": student.name, "id": student.id, "age": student.age, "classes": student.classes}
    write_to_db(create_student)
    return create_student


# get all students in a class
@app.get("/get-students-in-class/{class_name}", response_model=List[str])
def get_students_in_class(class_name: str = Path(..., description="The class that you would view its students")):
    """
    param class_name: the class name that through it we search about students
    return: a list of the students names that exist in a specific class(class_name)
    """
    students = read_from_db()
    class_students = []
    for stu in students:
        if class_name in stu["classes"]:
            class_students.append(stu["name"])
    if class_students:
        return class_students
    else:
        raise HTTPException(status_code=404, detail="No students found in this class")
