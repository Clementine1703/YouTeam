from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import applications
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi_pagination import add_pagination

from starlette.responses import RedirectResponse
from contextlib import asynccontextmanager

from apps.users.router import router as users_router
from apps.auth.router import router as auth_router
from apps.roles.router import router as roles_router
from apps.permissions.router import router as permissions_router

from config.config import APP_NAME, VERSION
from config.database import create_tables

from apps.users import router, models


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui-bundle.min.js",
        swagger_css_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui.min.css")

applications.get_swagger_ui_html = swagger_monkey_patch

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
    await create_tables()
    yield
    # Any shutdown code here

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(roles_router)
app.include_router(permissions_router)

add_pagination(app)
