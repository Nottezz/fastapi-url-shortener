from fastapi import Request

from storage.short_url import ShortUrlStorage


def get_short_url_storage(
    request: Request,
) -> ShortUrlStorage:
    return request.app.state.short_url_storage
