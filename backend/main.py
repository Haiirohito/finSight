from fastapi import FastAPI

from db.base import Base
from db.session import engine

# Models imports
from auth import models as auth_models

# Router imports
from auth.routes import router as auth_router

from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# Create tables on startup
Base.metadata.create_all(bind=engine)


# Register routers
app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "API is running"}
