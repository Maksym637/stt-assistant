from unittest.mock import MagicMock, patch

from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from tests.data.data import (
    to_iso_8601,
    TEST_HEADERS,
    TEST_PAYLOAD,
    TEST_USER,
    TEST_RECORD,
)


@patch("api.routes.record.generate_sas_url")
@patch("api.routes.record.get_blob_name_from_url")
@patch("api.routes.record.create_record")
@patch("api.routes.record.upload_to_blob")
@patch("api.routes.record.get_user_by_id")
def test_upload_audio_200(
    mock_get_user_by_id: MagicMock,
    mock_upload_to_blob: MagicMock,
    mock_create_record: MagicMock,
    mock_get_blob_name_from_url: MagicMock,
    mock_generate_sas_url: MagicMock,
    client_factory: TestClient,
):
    client: TestClient = client_factory(
        sub=TEST_PAYLOAD["sub"], email=TEST_PAYLOAD["email"]
    )

    mock_get_user_by_id.return_value = TEST_USER
    mock_upload_to_blob.return_value = "https://blob.example.com/first-phrase-en.mp3"
    mock_create_record.return_value = TEST_RECORD
    mock_get_blob_name_from_url.return_value = "first-phrase-en.mp3"
    mock_generate_sas_url.return_value = (
        "https://blob.example.com/first-phrase-en.mp3?sas_token"
    )

    response = client.post(
        url="/record/create",
        files={"file": ("audio1.wav", b"FAKEAUDIOCONTENT", "audio/wav")},
        headers=TEST_HEADERS,
    )

    assert mock_get_user_by_id.call_count == 1
    assert mock_upload_to_blob.call_count == 1
    assert mock_create_record.call_count == 1
    assert mock_get_blob_name_from_url.call_count == 1
    assert mock_generate_sas_url.call_count == 1

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "audio_url": TEST_RECORD.audio_url,
        "created_at": to_iso_8601(TEST_RECORD.created_at),
        "user_id": TEST_RECORD.user_id,
    }


@patch("core.auth.verify_jwt_token")
def test_upload_audio_401(mock_verify_jwt_token: MagicMock, client_factory: TestClient):
    client: TestClient = client_factory(
        sub=TEST_PAYLOAD["sub"],
        email=TEST_PAYLOAD["email"],
        is_authenticated=False,
    )

    mock_verify_jwt_token.side_effect = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
    )

    response = client.post(
        url="/record/create",
        files={"file": ("audio1.wav", b"FAKEAUDIOCONTENT", "audio/wav")},
        headers={"Authorization": "Bearer invalid_token"},
    )

    assert mock_verify_jwt_token.call_count == 1
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


@patch("api.routes.record.get_user_by_id")
def test_upload_audio_404(mock_get_user_by_id: MagicMock, client_factory: TestClient):
    client: TestClient = client_factory(
        sub=TEST_PAYLOAD["sub"], email=TEST_PAYLOAD["email"]
    )

    mock_get_user_by_id.return_value = None

    response = client.post(
        url="/record/create",
        files={"file": ("audio1.wav", b"FAKEAUDIOCONTENT", "audio/wav")},
        headers=TEST_HEADERS,
    )

    assert mock_get_user_by_id.call_count == 1
    assert response.status_code == 404
    assert response.json() == {"detail": "User's account not found"}


@patch("api.routes.record.get_user_by_id")
def test_upload_audio_invalid_file_400(
    mock_get_user_by_id: MagicMock, client_factory: TestClient
):
    client: TestClient = client_factory(
        sub=TEST_PAYLOAD["sub"], email=TEST_PAYLOAD["email"]
    )

    mock_get_user_by_id.return_value = TEST_USER

    response = client.post(url="/record/create", files={}, headers=TEST_HEADERS)

    assert mock_get_user_by_id.call_count == 1
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid or missing audio file"}


@patch("api.routes.record.upload_to_blob")
@patch("api.routes.record.get_user_by_id")
def test_upload_audio_existence_of_file_400(
    mock_get_user_by_id: MagicMock,
    mock_upload_to_blob: MagicMock,
    client_factory: TestClient,
):
    client: TestClient = client_factory(
        sub=TEST_PAYLOAD["sub"], email=TEST_PAYLOAD["email"]
    )

    mock_get_user_by_id.return_value = TEST_USER
    mock_upload_to_blob.return_value = None

    response = client.post(
        url="/record/create",
        files={"file": ("audio1.wav", b"FAKEAUDIOCONTENT", "audio/wav")},
        headers=TEST_HEADERS,
    )

    assert mock_get_user_by_id.call_count == 1
    assert mock_upload_to_blob.call_count == 1
    assert response.status_code == 400
    assert response.json() == {"detail": "Provided audio file already exists"}
