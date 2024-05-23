from typing import Annotated
from fastapi import FastAPI, File, UploadFile
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from v1.routes import cars

load_dotenv()

middleware = [
    Middleware(
        CORSMiddleware, 
        allow_origins=["*"],
        allow_credentials=True, 
        allow_methods=["*"], 
        allow_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)


@app.get("/")
def hello():
    return {"message": "Hello world"}


app.include_router(cars.router)
