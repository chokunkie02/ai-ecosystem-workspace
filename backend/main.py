from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.ai_router import ai_router
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
