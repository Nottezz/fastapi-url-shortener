from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from url_shortener.schemas.short_url import ShortUrl
from url_shortener.storage.short_url import ShortUrlStorage
from url_shortener.storage.short_url.crud import storage


def get_short_url_storage(
    request: Request,
) -> ShortUrlStorage:
    return request.app.state.short_url_storage


GetShortUrlStorage = Annotated[ShortUrlStorage, Depends(get_short_url_storage)]


def prefetch_short_url(slug: str) -> ShortUrl:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL <{slug}> not found.",
    )


UrlBySlug = Annotated[ShortUrl, Depends(prefetch_short_url)]
