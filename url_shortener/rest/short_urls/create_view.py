from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError

from url_shortener.dependencies.short_url import GetShortUrlStorage
from url_shortener.exceptions import ShortUrlAlreadyExistsError
from url_shortener.schemas.short_url import ShortUrlCreate
from url_shortener.services.short_urls.form_response_helper import FormResponseHelper

router = APIRouter(prefix="/create")
form_response = FormResponseHelper(
    model=ShortUrlCreate,
    template_name="short-urls/create.html",
)


@router.get("/", name="short-url:create-view")
def get_page_create_short_url(request: Request) -> HTMLResponse:
    return form_response.render(request)


@router.post("/", name="short-url:create", response_model=None)
async def add_short_url(
    request: Request, storage: GetShortUrlStorage
) -> HTMLResponse | RedirectResponse:
    async with request.form() as form:
        try:
            short_url_create = ShortUrlCreate.model_validate(form)
        except ValidationError as exc:
            return form_response.render(
                request=request,
                form_data=form,
                pydantic_error=exc,
                form_validated=True,
            )

    try:
        storage.create_or_raise_if_exists(short_url_create)
    except ShortUrlAlreadyExistsError:
        errors = {
            "slug": f"URL with '{short_url_create.slug}' already exists.",
        }
    else:
        return RedirectResponse(
            url=request.url_for("short-url:list-view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return form_response.render(
        request=request,
        errors=errors,
        form_data=short_url_create,
        form_validated=True,
    )
