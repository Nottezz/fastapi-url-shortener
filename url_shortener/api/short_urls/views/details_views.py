from typing import Annotated

from fastapi import APIRouter, Depends, status

from url_shortener.api.short_urls.crud import storage
from url_shortener.api.short_urls.dependencies import prefetch_short_url
from url_shortener.schemas.short_url import (
    ShortUrl,
    ShortUrlPartialUpdate,
    ShortUrlRead,
    ShortUrlUpdate,
)

router = APIRouter(prefix="/{slug}")

ShortUrlBySlug = Annotated[
    ShortUrl,
    Depends(prefetch_short_url),
]


@router.get(
    "/",
    response_model=ShortUrlRead,
)
def read_short_url_details(
    short_url: ShortUrlBySlug,
) -> ShortUrl:
    return short_url


@router.put(
    "/",
    response_model=ShortUrlRead,
)
def update_short_url_details(
    url: ShortUrlBySlug, short_url_in: ShortUrlUpdate
) -> ShortUrl:
    return storage.update(short_url=url, short_url_in=short_url_in)


@router.patch(
    "/",
    response_model=ShortUrlRead,
)
def partial_update_short_url_details(
    url: ShortUrlBySlug, short_url_in: ShortUrlPartialUpdate
) -> ShortUrl:
    return storage.update_partial(short_url=url, short_url_in=short_url_in)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_short_url(url: ShortUrlBySlug) -> None:
    storage.delete(short_url=url)
