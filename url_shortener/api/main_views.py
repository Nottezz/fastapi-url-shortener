from datetime import date, datetime
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from templating import templates
from url_shortener.schemas.health import Health

router = APIRouter()
app_launch_time = datetime.now()


@router.get("/", include_in_schema=False)
def root(request: Request) -> HTMLResponse:
    context: dict[str, Any] = {}
    today = date.today()
    features = [
        "Managing short URL: create, update, delete",
        "Custom alias for short links",
        "Analytics: track clicks, referrers, devices, and geolocation",
        "Expiration rules: set expiry date or maximum number of clicks",
        "Password-protected short links",
        "Bulk creation and import/export of short URLs",
    ]
    context.update(
        today=today,
        features=features,
    )
    return templates.TemplateResponse(
        request=request, name="home.html", context=context
    )


@router.get("/health")
def check_health() -> Health:
    uptime = (datetime.now() - app_launch_time).total_seconds()
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return Health(
        status="OK",
        current_date=datetime.now().isoformat(sep=" "),
        current_uptime=int(uptime),
        docs_url=str(docs_url),
    )
