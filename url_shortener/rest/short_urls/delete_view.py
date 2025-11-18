from fastapi import APIRouter, Response, status

from url_shortener.dependencies.short_url import GetShortUrlStorage, UrlBySlug

router = APIRouter(prefix="/{slug}/delete")


@router.delete("/", name="short-url:delete")
async def delete_short_url(
    storage: GetShortUrlStorage,
    url: UrlBySlug,
) -> Response:
    storage.delete(url)
    return Response(
        status_code=status.HTTP_200_OK,
        content="",
    )
