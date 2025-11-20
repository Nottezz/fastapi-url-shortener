import logging.config

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from url_shortener.api import router as api_router

# from url_shortener.api.main_views import router as main_router
from url_shortener.api.redirect_views import router as redirect_router
from url_shortener.app_lifespan import lifespan
from url_shortener.config import settings
from url_shortener.logging_config import LOGGING_CONFIG
from url_shortener.rest import router as rest_router

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI(
    lifespan=lifespan,
)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session.secret_key,
)
# app.include_router(main_router)
app.include_router(rest_router)
app.include_router(redirect_router)
app.include_router(api_router)
