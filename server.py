from fastapi import FastAPI
from routes import school_api

# creating server by fastapi, for get the requests from the endpoints in the school_api
server = FastAPI()
server.include_router(school_api.router)
