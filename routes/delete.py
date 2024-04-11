from fastapi import APIRouter, HTTPException, Depends

from auth.jwt_bearer import jwtBearer
from models.student_model import Student
from utils.auth_fns import is_admin
from read_write_db import read_from_db, write_to_db, write_to_db_after_delete
from logging_decerators.decorators import logger, log_request, log_success, log_error

router = APIRouter(
    tags=["Delete Student/s"]
)


# This route is used for delete all the students in the db. only admin(Depends) can do this operation
@router.delete("/delete/all-students", dependencies=[Depends(is_admin)])
@log_request
@log_success
@log_error
def delete_all_students():
    # Clear the list of students
    students = []
    # Write the empty list back to the database file
    write_to_db_after_delete(students)
    return {"message": "all students in database have been deleted"}


# This route is deleting a student by his id.
@router.delete("/delete/student-by-id/{student_id}", dependencies=[Depends(jwtBearer())])
@log_request
@log_success
@log_error
def delete_student_by_id(student_id: int):
    students = read_from_db()
    for index, stud in enumerate(students):
        if stud["id"] == student_id:
            # Remove the student from the list
            del students[index]
            # Write the updated list back to the database
            write_to_db_after_delete(students)
            return {"message": f"Student with ID {student_id} has been deleted"}
    raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
