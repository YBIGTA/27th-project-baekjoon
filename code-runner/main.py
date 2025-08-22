from fastapi import FastAPI
import uvicorn

from app.api import router
from app.config import PORT

app = FastAPI()

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
