from datetime import date

from fastapi import Request
from fastapi.templating import Jinja2Templates

from url_shortener.config import BASE_DIR
from url_shortener.misc.flash_messages import get_flashed_messages


def inject_current_date(
    request: Request,  # noqa: ARG001
) -> dict[str, date]:
    return {"today": date.today()}


templates = Jinja2Templates(
    directory=BASE_DIR / "templates",
    context_processors=[
        inject_current_date,
    ],
)

templates.env.globals["get_flashed_messages"] = get_flashed_messages
