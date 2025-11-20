from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError

from url_shortener.dependencies.short_url import GetShortUrlStorage, UrlBySlug
from url_shortener.misc.flash_messages import flash
from url_shortener.schemas.short_url import ShortUrlUpdate
from url_shortener.services.short_urls.form_response_helper import FormResponseHelper

router = APIRouter(prefix="/{slug}/update")
form_response = FormResponseHelper(
    model=ShortUrlUpdate,
    template_name="short-urls/update.html",
)


@router.get("/", name="short-url:update-view")
def get_page_update_short_url(
    request: Request,
    url: UrlBySlug,
) -> HTMLResponse:
    form = ShortUrlUpdate(**url.model_dump())
    return form_response.render(
        request=request,
        form_data=form,
        url=url,
    )


@router.post("/", name="short-url:update", response_model=None)
async def update_short_url(
    request: Request,
    storage: GetShortUrlStorage,
    url: UrlBySlug,
) -> HTMLResponse | RedirectResponse:
    async with request.form() as form:
        try:
            short_url_update = ShortUrlUpdate.model_validate(form)
        except ValidationError as exc:
            return form_response.render(
                request=request,
                form_data=form,
                pydantic_error=exc,
                form_validated=True,
                url=url,
            )

    storage.update(url, short_url_update)
    flash(
        request=request,
        message=f"Successfully updated {url.target_url}.",
        category="success",
    )
    return RedirectResponse(
        url=request.url_for("short-url:list-view"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
