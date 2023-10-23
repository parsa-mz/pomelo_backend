from typing import List

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from starlette.responses import RedirectResponse

from apps.transations.routers import router as transaction_router
from apps.users.routers import router as user_router
from core.dependencies.database import database
from core.settings import settings
from core.utils import p_g


def init_routers(app_: FastAPI) -> None:
    app_.include_router(transaction_router, prefix="/transactions")
    app_.include_router(user_router, prefix="/users")


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ]
    return middleware


def sentry_init():
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        # Needs adjustment for production,
        traces_sample_rate=1.0,
    )


def create_app() -> FastAPI:
    print("> Running in `{}` environment".format(p_g(settings.ENV)))

    app_ = FastAPI(
        title="Pomelo Backend server",
        description="Pomelo Backend server",
        version=settings.APP_VERSION,
        docs_url=None if settings.ENV == "production" else "/docs",
        redoc_url=None if settings.ENV == "production" else "/redoc",
        dependencies=[],
        middleware=make_middleware(),
    )
    init_routers(app_=app_)

    add_pagination(app_)

    database.connect()

    if settings.ENV == "prod":
        sentry_init()

    return app_


app = create_app()


@app.get("/", response_model=dict)
async def index():
    return RedirectResponse(url="/docs")

