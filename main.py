from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "You owe $10 for that book you never returned."}
