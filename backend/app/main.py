from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.user.user_router import user
from app.crawler.crawler_router import router as crawler_router
from app.config import PORT
from app.database_init import init_database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user)
app.include_router(crawler_router)

@app.get("/")
def root():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    """
    애플리케이션 시작 시 실행되는 이벤트
    """
    print("🚀 Starting BaekjoonHelper Backend...")
    init_database()

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)