from unittest.mock import MagicMock, patch

from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from tests.data.data import TEST_HEADERS, TEST_PAYLOAD, TEST_USER


@patch("api.routes.user.get_user_by_id")
def test_get_authenticated_user_200(
    mock_get_user_by_id: MagicMock, client_factory: TestClient
):
    client: TestClient = client_factory(
        sub=TEST_PAYLOAD["sub"], email=TEST_PAYLOAD["email"]
    )

    mock_get_user_by_id.return_value = TEST_USER

    response = client.get(url="/user/me", headers=TEST_HEADERS)

    assert mock_get_user_by_id.call_count == 1
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "auth0_id": TEST_PAYLOAD["sub"],
        "email": TEST_PAYLOAD["email"],
    }


@patch("api.routes.user.get_user_by_id")
def test_get_authenticated_user_404(
    mock_get_user_by_id: MagicMock, client_factory: TestClient
):
    client: TestClient = client_factory(
        sub=TEST_PAYLOAD["sub"], email=TEST_PAYLOAD["email"]
    )

    mock_get_user_by_id.return_value = None

    response = client.get(url="/user/me", headers=TEST_HEADERS)

    assert mock_get_user_by_id.call_count == 1
    assert response.status_code == 404
    assert response.json() == {"detail": "User's account not found"}


@patch("core.auth.verify_jwt_token")
def test_get_authenticated_user_401(
    mock_verify_jwt_token: MagicMock, client_factory: TestClient
):
    client: TestClient = client_factory(
        sub=TEST_PAYLOAD["sub"],
        email=TEST_PAYLOAD["email"],
        is_authenticated=False,
    )

    mock_verify_jwt_token.side_effect = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
    )

    response = client.get(
        url="/user/me", headers={"Authorization": "Bearer invalid_token"}
    )

    assert mock_verify_jwt_token.call_count == 1
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


@patch("api.routes.user.create_user")
@patch("api.routes.user.get_user_by_id")
def test_create_authenticated_user_account_200(
    mock_get_user_by_id: MagicMock,
    mock_create_user: MagicMock,
    client_factory: TestClient,
):
    client: TestClient = client_factory(
        sub=TEST_PAYLOAD["sub"], email=TEST_PAYLOAD["email"]
    )

    mock_get_user_by_id.return_value = None
    mock_create_user.return_value = TEST_USER

    response = client.post(url="/user/create", headers=TEST_HEADERS)

    assert mock_get_user_by_id.call_count == 1
    assert mock_create_user.call_count == 1

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "auth0_id": TEST_PAYLOAD["sub"],
        "email": TEST_PAYLOAD["email"],
    }


@patch("api.routes.user.get_user_by_id")
def test_create_authenticated_user_account_409(
    mock_get_user_by_id: MagicMock, client_factory: TestClient
):
    client: TestClient = client_factory(
        sub=TEST_PAYLOAD["sub"], email=TEST_PAYLOAD["email"]
    )

    mock_get_user_by_id.return_value = TEST_USER

    response = client.post(url="/user/create", headers=TEST_HEADERS)

    assert mock_get_user_by_id.call_count == 1
    assert response.status_code == 409
    assert response.json() == {"detail": "User's account already exists"}
