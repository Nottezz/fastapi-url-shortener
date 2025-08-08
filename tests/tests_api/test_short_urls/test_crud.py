import pytest
from pydantic import AnyHttpUrl
from url_shortener.api.short_urls.crud import storage
from url_shortener.exceptions import ShortUrlAlreadyExistsError
from url_shortener.schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlPartialUpdate,
    ShortUrlUpdate,
)

from ..conftest import build_short_url_create_random_slug


class TestShortUrlStorageGetBySlug:
    def test_get_short_url_by_slug(self, short_url: ShortUrl) -> None:
        result = storage.get_by_slug(slug=short_url.slug)
        assert result.target_url == AnyHttpUrl("https://example.com/")  # type: ignore[union-attr]
        assert result.summary == "A short url"  # type: ignore[union-attr]


class TestShortUrlStorageExists:
    def test_check_short_url_exists(self, short_url: ShortUrl) -> None:
        result = storage.exists(slug=short_url.slug)
        assert result == True


class TestShortUrlStorageCreate:
    def test_create_short_url(self, short_url: ShortUrl) -> None:
        short_url_create = ShortUrlCreate(**short_url.model_dump())
        result = storage.create(short_url_create)
        assert result.slug == short_url.slug
        assert result.target_url == short_url.target_url
        assert result.summary == short_url.summary

    def test_create_or_raise_if_exists(self, short_url: ShortUrl) -> None:
        short_url_create = ShortUrlCreate(**short_url.model_dump())
        with pytest.raises(
            ShortUrlAlreadyExistsError,
            match=short_url_create.slug,
        ) as exc_info:
            storage.create_or_raise_if_exists(short_url_create)

        assert exc_info.value.args[0] == short_url_create.slug

    def test_create_twice(self) -> None:
        short_url_create = build_short_url_create_random_slug()
        storage.create_or_raise_if_exists(short_url_create)

        with pytest.raises(
            ShortUrlAlreadyExistsError,
            match=short_url_create.slug,
        ) as exc_info:
            storage.create_or_raise_if_exists(short_url_create)
        assert exc_info.value.args == (short_url_create.slug,)


class TestShortUrlStorageUpdate:
    def test_update_short_url(self, short_url: ShortUrl) -> None:
        short_url_update = ShortUrlUpdate(**short_url.model_dump())
        source_summary = short_url.summary

        short_url_update.summary *= 2
        updated_short_url = storage.update(
            short_url=short_url,
            short_url_in=short_url_update,
        )

        assert source_summary != short_url.summary
        assert short_url_update == ShortUrlUpdate(**updated_short_url.model_dump())

    def test_partial_update_short_url(self, short_url: ShortUrl) -> None:
        short_url_partial_update = ShortUrlPartialUpdate(
            summary=short_url.summary * 2,
        )
        source_summary = short_url.summary
        updated_short_url = storage.update_partial(
            short_url=short_url,
            short_url_in=short_url_partial_update,
        )

        assert source_summary != short_url.summary
        assert short_url_partial_update.summary == updated_short_url.summary
