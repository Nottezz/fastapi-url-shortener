from fastapi import APIRouter
from starlette.responses import RedirectResponse

from url_shortener.dependencies.short_url import UrlBySlug

router = APIRouter(
    prefix="/redirect",
    tags=["Redirect"],
)


@router.get("")
@router.get("/")
def redirect_short_url(
    url: UrlBySlug,
) -> RedirectResponse:
    return RedirectResponse(
        url=str(url.target_url),
    )
