from fastapi import FastAPI
import uvicorn

from app.config import PORT
from app.api.api_router import solve_router

app = FastAPI()

app.include_router(solve_router)

@app.get("/")
def health():
    return {"status": "ok"}

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)