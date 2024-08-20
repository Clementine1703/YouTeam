from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from contextlib import asynccontextmanager


from backend.src.apps import users

from src.config.config import APP_NAME, VERSION
from src.config.database import engine

from src.apps.users import router, models
# from src.routes.auth import main, models

users.models.Base.metadata.create_all(bind=engine)
# auth.models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=APP_NAME,
    version=VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(users.router.router)

# Redirect / -> Swagger-UI documentation
@app.get("/")
def main_function():
    """
    # Redirect
    to documentation (`/docs/`).
    """
    return RedirectResponse(url="/docs/")