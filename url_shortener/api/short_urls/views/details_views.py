from fastapi import APIRouter, status

from dependencies.short_url import UrlBySlug
from storage.short_url.crud import storage
from url_shortener.schemas.short_url import (
    ShortUrl,
    ShortUrlPartialUpdate,
    ShortUrlRead,
    ShortUrlUpdate,
)

router = APIRouter(prefix="/{slug}")


@router.get(
    "/",
    response_model=ShortUrlRead,
)
def read_short_url_details(
    short_url: UrlBySlug,
) -> ShortUrl:
    return short_url


@router.put(
    "/",
    response_model=ShortUrlRead,
)
def update_short_url_details(url: UrlBySlug, short_url_in: ShortUrlUpdate) -> ShortUrl:
    return storage.update(short_url=url, short_url_in=short_url_in)


@router.patch(
    "/",
    response_model=ShortUrlRead,
)
def partial_update_short_url_details(
    url: UrlBySlug, short_url_in: ShortUrlPartialUpdate
) -> ShortUrl:
    return storage.update_partial(short_url=url, short_url_in=short_url_in)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_short_url(url: UrlBySlug) -> None:
    storage.delete(short_url=url)
