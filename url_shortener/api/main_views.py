from datetime import datetime

from fastapi import APIRouter, Request

from url_shortener.schemas.health import Health

router = APIRouter()
app_launch_time = datetime.now()


@router.get("/")
def root(
    request: Request,
) -> Health:
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
