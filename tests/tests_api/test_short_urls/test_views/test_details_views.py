from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient
from pydantic import AnyHttpUrl
from url_shortener.main import app
from url_shortener.schemas.short_url import ShortUrl, ShortUrlUpdate
from url_shortener.storage.short_url.crud import storage

from tests.tests_api.conftest import create_short_url, create_short_url_random_slug

pytestmark = pytest.mark.apitest


class TestShortenerGetShortUrl:
    def test_shortener_get_details(
        self, client: TestClient, short_url: ShortUrl
    ) -> None:
        url = app.url_path_for("read_short_url_details", slug=short_url.slug)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK, response.text
        response_json = response.json()
        assert response_json == short_url.model_dump(mode="json"), response_json

    def test_shortener_get_details_unknown_slug(self, client: TestClient) -> None:
        url = app.url_path_for("read_short_url_details", slug="unknown_slug")
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
        response_json = response.json()
        expected_error_detail = f"URL <unknown_slug> not found."
        assert response_json["detail"] == expected_error_detail, response_json


class TestShortenerUpdateShortUrl:
    @pytest.fixture
    def short_url(self, request: SubRequest) -> Generator[ShortUrl, None, None]:
        summary, target_url = request.param
        short_url = create_short_url_random_slug(summary, target_url)
        yield short_url
        storage.delete(short_url)

    @pytest.mark.parametrize(
        ("short_url", "new_target_url", "new_summary"),
        [
            pytest.param(
                ("a" * 10, "https://fgs.example.com"),
                AnyHttpUrl("https://abc.example.com"),
                "example with second domain lvl",
                id="min-summary",
            ),
            pytest.param(
                ("a" * 100, "https://qwe.example.com"),
                AnyHttpUrl("https://qwerty.example.com"),
                "qwerty example url",
                id="max-summary",
            ),
        ],
        indirect=["short_url"],
    )
    def test_update_short_url_detailed(
        self,
        client: TestClient,
        short_url: ShortUrl,
        new_target_url: str,
        new_summary: str,
    ) -> None:
        url = app.url_path_for("update_short_url_details", slug=short_url.slug)
        shortener_before_update = storage.get_by_slug(short_url.slug)
        short_url_update = ShortUrlUpdate(
            target_url=new_target_url,
            summary=new_summary,
        ).model_dump(mode="json")

        response = client.put(url, json=short_url_update)
        assert response.status_code == status.HTTP_200_OK, response.text

        short_url_from_db = storage.get_by_slug(short_url.slug)
        assert short_url_from_db != shortener_before_update
        assert short_url_from_db.summary == new_summary  # type: ignore [union-attr]
        assert short_url_from_db.target_url == new_target_url  # type: ignore [union-attr]


class TestShortenerPartialUpdateShortUrl:
    @pytest.fixture
    def short_url(self, request: SubRequest) -> Generator[ShortUrl, None, None]:
        short_url = create_short_url_random_slug(summary=request.param)
        yield short_url
        storage.delete(short_url)

    @pytest.mark.parametrize(
        ("short_url", "new_summary"),
        [
            pytest.param(
                "a" * 10,
                "a" * 100,
                id="min-summary-to-max-summary",
            ),
            pytest.param(
                "a" * 100,
                "a" * 10,
                id="max-summary-to-min-summary",
            ),
        ],
        indirect=["short_url"],
    )
    def test_partial_update_short_url_detailed(
        self,
        client: TestClient,
        short_url: ShortUrl,
        new_summary: str,
    ) -> None:
        url = app.url_path_for("partial_update_short_url_details", slug=short_url.slug)
        shortener_before_update = storage.get_by_slug(short_url.slug)

        response = client.patch(url, json={"summary": new_summary})
        assert response.status_code == status.HTTP_200_OK, response.text

        short_url_from_db = storage.get_by_slug(short_url.slug)
        assert short_url_from_db != shortener_before_update
        assert short_url_from_db.summary == new_summary  # type: ignore[union-attr]


class TestShortenerDeleteShortUrl:
    @pytest.fixture(
        params=[
            pytest.param(
                "abc",
                id="minimal-slug",
            ),
            pytest.param(
                "abcdefgh",
                id="default-slug",
            ),
            pytest.param(
                "a" * 10,
                id="max-slug",
            ),
        ]
    )
    def short_url(self, request: SubRequest) -> Generator[ShortUrl, None, None]:
        short_url = create_short_url(slug=request.param)
        yield short_url
        storage.delete(short_url)

    def test_delete_short_url(self, client: TestClient, short_url: ShortUrl) -> None:
        url = app.url_path_for("delete_short_url", slug=short_url.slug)
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
        assert not storage.exists(short_url.slug)
