import pytest
from fastapi import status
from fastapi.testclient import TestClient

pytestmark = pytest.mark.apitest


def test_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK, response.text
    response_json = response.json()
    assert response_json["status"] == "OK", response_json
    assert response_json["current_uptime"] == 0, response_json
    assert response_json["docs_url"] == "http://testserver/docs", response_json
