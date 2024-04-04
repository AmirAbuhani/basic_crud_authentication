from typing import List
from fastapi import APIRouter, Path, HTTPException, Depends
from read_write_db import read_from_db, write_to_db
from models.student_model import Student
from auth.jwt_bearer import jwtBearer
from routes.sign_in_up import is_admin

# creating api router, for using it to define endpoints later
router = APIRouter()


# This route retrieves all students from the database. It requires JWT token authentication,
# ensuring only authenticated users can access this endpoint
@router.get("/all-students", response_model=List[Student], dependencies=[Depends(jwtBearer())],
            tags=["student functionality"])
def get_all_students():
    students = read_from_db()
    return students


# This route retrieves a specific student by their ID from the database. It requires JWT token authentication
@router.get("/get-student/{student_id}", response_model=Student, dependencies=[Depends(jwtBearer())], tags=["student "
                                                                                                            "functionality"])
def get_student(student_id: int = Path(..., description="The ID of the student you would like to view")):

    students = read_from_db()
    for student in students:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student id not found")


# This route adds a new student to the database. It requires admin authentication,
# which is checked using the is_admin dependency.
@router.post("/add-student", dependencies=[Depends(is_admin)], response_model=Student, tags=["student functionality"])
def add_student(student_id: int, student: Student):
    students = read_from_db()
    students_ids = []
    for stu in students:
        students_ids.append(stu["id"])
    if student_id in students_ids:
        raise HTTPException(status_code=400, detail="Student id is already exists.")
    create_student = {"name": student.name, "id": student.id, "age": student.age, "classes": student.classes}
    write_to_db(create_student)
    return create_student


# This route retrieves all students belonging to a specific class from the database. It requires admin authentication
@router.get("/get-students-in-class/{class_name}", dependencies=[Depends(is_admin)], response_model=List[str],
            tags=["student functionality"])
def get_students_in_class(class_name: str = Path(..., description="The class that you would view its students")):
    students = read_from_db()
    class_students = []
    for stu in students:
        if class_name in stu["classes"]:
            class_students.append(stu["name"])
    if class_students:
        return class_students
    else:
        raise HTTPException(status_code=404, detail="No students found in this class")
