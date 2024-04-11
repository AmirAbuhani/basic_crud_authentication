# This module is for reading and writing from/to students_db.json file
import json


# read students from students_db
def read_from_db():
    """
    return:
        the dictionary of the students or empty list if there is an error file
    """
    try:
        with open("data/students_db.json", "r") as file:
            return json.load(file)["students"]
    except FileNotFoundError:
        return {"students": []}


# write students to students_db
def write_to_db(student):
    # Load existing data
    try:
        with open("data/students_db.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"students": []}

    # Append new student to the list
    data["students"].append(student)

    # Write updated data back to the file
    with open("data/students_db.json", "w") as file:
        json.dump(data, file, indent=2)


def write_to_db_after_delete(students):
    with open("data/students_db.json", "w") as file:
        json.dump({"students": students}, file, indent=2)
