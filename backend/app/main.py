from fastapi import FastAPI

from app.routers import task

app = FastAPI()


@app.get("/hello")
async def hello():
    return {"message": "Hello World"}


app.include_router(task.router)
