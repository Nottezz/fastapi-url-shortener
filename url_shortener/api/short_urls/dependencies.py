from fastapi import HTTPException, status

from url_shortener.api.short_urls.crud import storage
from url_shortener.schemas.short_url import ShortUrl


def prefetch_short_url(slug: str) -> ShortUrl:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL <{slug}> not found.",
    )
