from fastapi import FastAPI

from api.routers import done, task

app = FastAPI()


@app.get("/hello")
async def hello():
    return {"message": "Hello World"}


app.include_router(task.router)
app.include_router(done.router)
