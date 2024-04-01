Author: Amir Abu Hani

The aim of this project is to build a server(using fastapi) to response to the user requests(endpoints).
we have a database called students_db.json that include all the students. from this db, the server can read and write to
it.

By the 2 functions in the read_write_db module, we can access to the db.

The main module is the school_api. at first, I create an instance of routeAPI(router) that listening for incoming HTTP 
requests and responds. by the server module, I create an instance of fastAPI, through it, we can activate the server.
I'm also create a Student class that inherits from the BaseModel class using pydantic. We have 4 endpoints:

1- GET /all-students: Returns a list of all students.

2- GET /get-student/{student_id}: Returns details of a specific student by their ID.

3- POST /add-student: Adds a new student.

4- GET /get-students-in-class/{class_name}: Returns names of students belonging to a specific class.

To activate the server, I used the command "uvicon school_api:app --reload" at pycharm terminal, then in the browser
I'm type http://127.0.0.1:8000/docs . then the 4 endpoints will appear, and I can do the relevant request according
to the endpoint aim.

![school_api](endpoints.jpg)