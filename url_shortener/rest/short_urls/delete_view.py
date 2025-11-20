from fastapi import APIRouter, Request, Response, status

from url_shortener.dependencies.short_url import GetShortUrlStorage, UrlBySlug
from url_shortener.misc.flash_messages import flash

router = APIRouter(prefix="/{slug}/delete")


@router.delete("/", name="short-url:delete")
async def delete_short_url(
    storage: GetShortUrlStorage,
    url: UrlBySlug,
    request: Request,
) -> Response:
    storage.delete(url)
    flash(
        request=request,
        message=f"Successfully deleted {url.target_url}.",
        category="danger",
    )
    return Response(
        status_code=status.HTTP_200_OK,
        content="",
    )
