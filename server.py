# Author: Amir Abu Hani
from fastapi import FastAPI
from routes import school_api, sign_in_up, delete, chat_websocket

# creating server using fastapi, for get the requests from the endpoints in the school_api and the sign_in_up
server = FastAPI()
server.include_router(sign_in_up.router)
server.include_router(school_api.router)
server.include_router(delete.router)
server.include_router(chat_websocket.router)

