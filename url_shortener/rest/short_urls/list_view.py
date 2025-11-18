from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from url_shortener.dependencies.short_url import GetShortUrlStorage
from url_shortener.templating import templates

router = APIRouter()


@router.get("/", name="short-url:list-view")
def list_view(request: Request, storage: GetShortUrlStorage) -> HTMLResponse:
    context: dict[str, Any] = {}
    list_urls = storage.get()
    context.update(list_urls=list_urls)
    return templates.TemplateResponse(
        request=request,
        name="short-urls/list.html",
        context=context,
    )
