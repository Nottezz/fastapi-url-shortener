from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from storage.short_url import ShortUrlStorage
from url_shortener.config import settings


@asynccontextmanager
async def lifespan(
    app: FastAPI,  # noqa: ARG001
) -> AsyncIterator[None]:
    app.state.short_url_storage = ShortUrlStorage(
        hash_name=settings.redis.collections.url_shortener_hash
    )
    yield
