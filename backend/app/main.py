from fastapi import FastAPI
import uvicorn

from app.user.user_router import user
from app.config import PORT

app = FastAPI()

app.include_router(user)

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)