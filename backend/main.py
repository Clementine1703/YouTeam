from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from contextlib import asynccontextmanager


from src.apps import users

from src.config.config import APP_NAME, VERSION
from src.config.database import engine, create_tables

from src.apps.users import router, models
# from src.routes.auth import main, models


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

@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.apps.users.service import check_db_connection
    await create_tables()
    await check_db_connection()
    yield
    # Any shutdown code here

app.include_router(users.router.router)

# Redirect / -> Swagger-UI documentation
@app.get("/")
def main_function():
    """
    # Redirect
    to documentation (`/docs/`).
    """
    return RedirectResponse(url="/docs/")