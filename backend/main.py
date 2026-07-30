from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import item_router
from backend.core.config import settings

app = FastAPI(title=settings.project_name, version=settings.version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(item_router.router)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.project_name}"}
