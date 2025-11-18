import random
import string
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from pydantic import AnyHttpUrl
from url_shortener.main import app
from url_shortener.schemas.short_url import ShortUrl, ShortUrlCreate
from url_shortener.storage.short_url.crud import storage


@pytest.fixture
def client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client


def build_short_url_create(
    slug: str,
    summary: str = "A short url",
    target_url: str | AnyHttpUrl = "https://example.com",
) -> ShortUrlCreate:
    return ShortUrlCreate(
        slug=slug,
        summary=summary,
        target_url=target_url,
    )


def build_short_url_create_random_slug(
    description: str = "A short url",
    target_url: str | AnyHttpUrl = "https://example.com",
) -> ShortUrlCreate:
    return build_short_url_create(
        slug="".join(
            random.choices(  # noqa:  S311 Standard pseudo-random generators are not suitable for cryptographic purposes
                string.ascii_letters,
                k=8,
            ),
        ),
        summary=description,
        target_url=target_url,
    )


def create_short_url(
    slug: str,
    description: str = "A short url",
    target_url: str | AnyHttpUrl = "https://example.com",
) -> ShortUrl:
    short_url_in = build_short_url_create(
        slug=slug,
        summary=description,
        target_url=target_url,
    )
    return storage.create(short_url_in)


def create_short_url_random_slug(
    summary: str = "A short url",
    target_url: str | AnyHttpUrl = "https://example.com",
) -> ShortUrl:
    short_url_in = build_short_url_create_random_slug(
        description=summary,
        target_url=target_url,
    )
    return storage.create(short_url_in)


@pytest.fixture
def short_url() -> Generator[ShortUrl]:
    short_url = create_short_url_random_slug()
    yield short_url
    storage.delete(short_url)
