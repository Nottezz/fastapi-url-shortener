import logging

from fastapi import FastAPI

from app_lifespan import lifespan
from url_shortener.api import router as api_router
from url_shortener.api.main_views import router as main_router
from url_shortener.api.redirect_views import router as redirect_router
from url_shortener.config import settings

logging.basicConfig(
    level=settings.logging.log_level,
    format=settings.logging.log_format,
    datefmt=settings.logging.log_date_format,
)

app = FastAPI(
    lifespan=lifespan,
)
app.include_router(main_router)
app.include_router(redirect_router)
app.include_router(api_router)
