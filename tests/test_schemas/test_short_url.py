import pytest
from pydantic import ValidationError

from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlPartialUpdate,
    ShortUrlUpdate,
)


class TestShortUrlCreate:
    def test_short_url_can_be_created_from_create_schema(self) -> None:
        short_url_in = ShortUrlCreate(
            target_url="https://example.com",
            summary="link to example domain",
            slug="example",
        )
        short_url = ShortUrl(**short_url_in.model_dump())

        assert short_url_in.target_url == short_url.target_url
        assert short_url_in.summary == short_url.summary
        assert short_url_in.slug == short_url.slug

    @pytest.mark.parametrize(
        "url",
        [
            pytest.param("https://example", id="invalid-url"),
            pytest.param("http://abc.example.com", id="second-lvl-url"),
            pytest.param("https://www.example.com/foobar/", id="url-with-path"),
        ],
    )
    def test_short_url_create_accepts_different_urls(self, url: str) -> None:
        short_url_in = ShortUrlCreate(
            target_url=url, summary="link to example domain", slug="example"
        )

        short_url = ShortUrl(**short_url_in.model_dump())

        assert short_url_in.target_url == short_url.target_url

    @pytest.mark.parametrize(
        ("url", "summary", "slug", "should_raise"),
        [
            pytest.param(
                "https://example.com", "a" * 9, "a" * 2, True, id="values-less-than-min"
            ),
            pytest.param(
                "https://example.com", "a" * 10, "a" * 3, False, id="minimum-values"
            ),
            pytest.param(
                "https://example.com", "a" * 100, "a" * 10, False, id="maximum-values"
            ),
            pytest.param(
                "https://example.com",
                "a" * 101,
                "a" * 11,
                True,
                id="values-higher-than-max",
            ),
        ],
    )
    def test_short_url_max_and_min_value(
        self,
        url: str,
        summary: str,
        slug: str,
        should_raise: bool,
    ) -> None:
        if should_raise:
            with pytest.raises(ValidationError):
                ShortUrlCreate(
                    target_url=url,
                    summary=summary,
                    slug=slug,
                )
        else:
            short_url_in = ShortUrlCreate(
                target_url=url,
                summary=summary,
                slug=slug,
            )
            short_url = ShortUrl(**short_url_in.model_dump())
            assert short_url.summary == summary
            assert short_url.slug == slug


class TestShortUrlUpdate:
    def test_short_url_can_be_update_from_update_schema(self) -> None:
        short_url = ShortUrl(
            target_url="https://example.com",
            summary="link to example domain",
            slug="example",
        )

        short_url_update = ShortUrlUpdate(
            target_url="https://abc.example.com",
            summary="link to second lvl example domain",
        )

        for field, value in short_url_update:
            setattr(short_url, field, value)

        assert short_url_update.target_url == short_url.target_url
        assert short_url_update.summary == short_url.summary


class TestShortUrlPartialUpdate:
    def test_short_url_can_be_partial_updated_from_schema(self) -> None:
        short_url = ShortUrl(
            target_url="https://example.com",
            summary="link to example domain",
            slug="example",
        )

        short_url_partial_update = ShortUrlPartialUpdate(
            summary="updated summary",
        )

        for field, value in short_url_partial_update:
            setattr(short_url, field, value)

        assert short_url_partial_update.summary == short_url.summary
