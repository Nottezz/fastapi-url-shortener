from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from url_shortener.api.short_urls.dependencies import prefetch_short_url
from url_shortener.schemas.short_url import ShortUrl

router = APIRouter(
    prefix="/redirect",
    tags=["Redirect"],
)


@router.get("/{slug}")
@router.get("/{slug}/")
def redirect_short_url(
    url: Annotated[ShortUrl, Depends(prefetch_short_url)],
) -> RedirectResponse:
    return RedirectResponse(
        url=str(url.target_url),
    )
