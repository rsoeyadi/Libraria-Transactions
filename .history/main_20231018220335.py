from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "This microservice is for our library catalog."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
