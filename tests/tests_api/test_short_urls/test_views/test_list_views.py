import logging
import random
import string
from typing import Any

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient
from url_shortener.main import app

from schemas.short_url import ShortUrl, ShortUrlCreate
from tests_api.conftest import build_short_url_create_random_slug

pytestmark = pytest.mark.apitest


class TestShortenerGetList:
    def test_shortener_get_list(
        self,
        client: TestClient,
        short_url: ShortUrl,  # noqa:  ARG002 Unused method argument: `short_url`
    ) -> None:
        url = app.url_path_for("get_short_url_list")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK


class TestShortenerCreate:
    def test_shortener_create(
        self,
        client: TestClient,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        caplog.set_level(logging.DEBUG)
        url = app.url_path_for("create_short_url")
        short_url_create = ShortUrlCreate(
            slug="".join(
                random.choices(  # noqa: S311  Standard pseudo-random generators are not suitable for cryptographic purposes
                    string.ascii_letters,
                    k=10,
                ),
            ),
            summary="example short url for test",
            target_url="https://example.com",
        )
        data = short_url_create.model_dump(mode="json")
        response = client.post(url, json=data)

        assert response.status_code == status.HTTP_201_CREATED, response.text

        received_data = ShortUrlCreate(**response.json())
        assert received_data == short_url_create, received_data
        assert f"Created short url <{received_data.slug}>" in caplog.text

    def test_create_short_url_already_exists(
        self, client: TestClient, short_url: ShortUrl
    ) -> None:
        short_url_create = ShortUrlCreate(**short_url.model_dump()).model_dump(
            mode="json"
        )
        url = app.url_path_for("create_short_url")
        response = client.post(url, json=short_url_create)

        assert response.status_code == status.HTTP_409_CONFLICT, response.text
        response_json = response.json()
        expected_error_detail = (
            f"Short URL with slug <{short_url.slug}> already exists."
        )
        assert response_json["detail"] == expected_error_detail, response_json


class TestShortenerInvalid:
    @pytest.fixture(
        params=[
            pytest.param(("a", "string_too_short"), id="string_too_short"),
            pytest.param(("a" * 11, "string_too_long"), id="string_too_long"),
        ]
    )
    def short_url_create_values(
        self, request: SubRequest
    ) -> tuple[dict[str, Any], str]:
        build = build_short_url_create_random_slug()
        data = build.model_dump(mode="json")
        slug, err_type = request.param
        data["slug"] = slug
        return data, err_type

    def test_invalid_slug(
        self, client: TestClient, short_url_create_values: tuple[dict[str, Any], str]
    ) -> None:
        url = app.url_path_for("create_short_url")
        created_data, expected_error_type = short_url_create_values
        response = client.post(url, json=created_data)
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text
        error_detail = response.json().get("detail")[0]
        assert error_detail["type"] == expected_error_type, error_detail
