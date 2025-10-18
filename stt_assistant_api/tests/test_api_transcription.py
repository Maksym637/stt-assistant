from unittest.mock import MagicMock, patch

from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from tests.data.data import (
    to_iso_8601,
    tst_get_blob_name_from_url,
    tst_generate_sas_url,
    TEST_HEADERS,
    TEST_PAYLOAD,
    TEST_USER,
    TEST_RECORD,
    TEST_TRANSCRIPTION,
    TEST_TRANSCRIPTION_ALL_DB,
)


@patch("api.routes.transcription.create_transcription")
@patch("api.routes.transcription.transcribe_audio")
@patch("api.routes.transcription.get_blob_name_from_url")
@patch("api.routes.transcription.get_transcription_by_record_id")
@patch("api.routes.transcription.get_record_by_id")
@patch("api.routes.transcription.get_user_by_id")
def test_process_record_200(
    mock_get_user_by_id: MagicMock,
    mock_get_record_by_id: MagicMock,
    mock_get_transcription_by_record_id: MagicMock,
    mock_get_blob_name_from_url: MagicMock,
    mock_transcribe_audio: MagicMock,
    mock_create_transcription: MagicMock,
    client_factory: TestClient,
):
    client: TestClient = client_factory(
        sub=TEST_PAYLOAD["sub"], email=TEST_PAYLOAD["email"]
    )

    mock_get_user_by_id.return_value = TEST_USER
    mock_get_record_by_id.return_value = TEST_RECORD
    mock_get_transcription_by_record_id.return_value = None
    mock_get_blob_name_from_url.return_value = "first-phrase-en.mp3"
    mock_transcribe_audio.return_value = "Transcription text 1"
    mock_create_transcription.return_value = TEST_TRANSCRIPTION

    response = client.post(
        url="/transcription/create",
        json={"record_id": 1, "language_code": "en-US"},
        headers=TEST_HEADERS,
    )

    assert mock_get_user_by_id.call_count == 1
    assert mock_get_record_by_id.call_count == 1
    assert mock_get_transcription_by_record_id.call_count == 1
    assert mock_get_blob_name_from_url.call_count == 1
    assert mock_transcribe_audio.call_count == 1
    assert mock_create_transcription.call_count == 1

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "language_code": TEST_TRANSCRIPTION.language_code,
        "transcription": TEST_TRANSCRIPTION.transcription,
        "created_at": to_iso_8601(TEST_TRANSCRIPTION.created_at),
        "record_id": 1,
    }


@patch("api.routes.transcription.get_user_by_id")
def test_process_record_language_code_400(
    mock_get_user_by_id: MagicMock, client_factory: TestClient
):
    client: TestClient = client_factory(
        sub=TEST_PAYLOAD["sub"], email=TEST_PAYLOAD["email"]
    )

    mock_get_user_by_id.return_value = TEST_USER

    response = client.post(
        url="/transcription/create",
        json={"record_id": 1, "language_code": "na-NA"},
        headers=TEST_HEADERS,
    )

    assert mock_get_user_by_id.call_count == 1
    assert response.status_code == 400
    assert response.json() == {"detail": "Provided language code is not supported"}


@patch("api.routes.transcription.get_transcription_by_record_id")
@patch("api.routes.transcription.get_record_by_id")
@patch("api.routes.transcription.get_user_by_id")
def test_process_record_transcription_with_record_400(
    mock_get_user_by_id: MagicMock,
    mock_get_record_by_id: MagicMock,
    mock_get_transcription_by_record_id: MagicMock,
    client_factory: TestClient,
):
    client: TestClient = client_factory(
        sub=TEST_PAYLOAD["sub"], email=TEST_PAYLOAD["email"]
    )

    mock_get_user_by_id.return_value = TEST_USER
    mock_get_record_by_id.return_value = TEST_RECORD
    mock_get_transcription_by_record_id.return_value = TEST_TRANSCRIPTION

    response = client.post(
        url="/transcription/create",
        json={"record_id": 1, "language_code": "en-US"},
        headers=TEST_HEADERS,
    )

    assert mock_get_user_by_id.call_count == 1
    assert mock_get_record_by_id.call_count == 1
    assert mock_get_transcription_by_record_id.call_count == 1

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Transcription with the provided record already exists"
    }


@patch("core.auth.verify_jwt_token")
def test_process_record_401(
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

    response = client.post(
        url="/transcription/create",
        json={"record_id": 1, "language_code": "en-US"},
        headers={"Authorization": "Bearer invalid_token"},
    )

    assert mock_verify_jwt_token.call_count == 1
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


@patch("api.routes.transcription.get_record_by_id")
@patch("api.routes.transcription.get_user_by_id")
def test_process_record_record_not_found_404(
    mock_get_user_by_id: MagicMock,
    mock_get_record_by_id: MagicMock,
    client_factory: TestClient,
):
    client: TestClient = client_factory(
        sub=TEST_PAYLOAD["sub"], email=TEST_PAYLOAD["email"]
    )

    mock_get_user_by_id.return_value = TEST_USER
    mock_get_record_by_id.return_value = None

    response = client.post(
        url="/transcription/create",
        json={"record_id": 1, "language_code": "en-US"},
        headers=TEST_HEADERS,
    )

    assert mock_get_user_by_id.call_count == 1
    assert mock_get_record_by_id.call_count == 1
    assert response.status_code == 404
    assert response.json() == {"detail": "Record not found"}


@patch("api.routes.transcription.get_user_by_id")
def test_process_record_user_not_found_404(
    mock_get_user_by_id: MagicMock, client_factory: TestClient
):
    client: TestClient = client_factory(
        sub=TEST_PAYLOAD["sub"], email=TEST_PAYLOAD["email"]
    )

    mock_get_user_by_id.return_value = None

    response = client.post(
        url="/transcription/create",
        json={"record_id": 1, "language_code": "en-US"},
        headers=TEST_HEADERS,
    )

    assert mock_get_user_by_id.call_count == 1
    assert response.status_code == 404
    assert response.json() == {"detail": "User's account not found"}


@patch("api.routes.transcription.generate_sas_url")
@patch("api.routes.transcription.get_blob_name_from_url")
@patch("api.routes.transcription.get_transcriptions_by_user_id")
@patch("api.routes.transcription.get_user_by_id")
def test_get_all_transcriptions_200(
    mock_get_user_by_id: MagicMock,
    mock_get_transcriptions_by_user_id: MagicMock,
    mock_get_blob_name_from_url: MagicMock,
    mock_generate_sas_url: MagicMock,
    client_factory: TestClient,
):
    client: TestClient = client_factory(
        sub=TEST_PAYLOAD["sub"], email=TEST_PAYLOAD["email"]
    )

    mock_get_user_by_id.return_value = TEST_USER
    mock_get_transcriptions_by_user_id.return_value = TEST_TRANSCRIPTION_ALL_DB
    mock_get_blob_name_from_url.side_effect = tst_get_blob_name_from_url
    mock_generate_sas_url.side_effect = tst_generate_sas_url

    response = client.get(url="/transcription/all", headers=TEST_HEADERS)

    assert mock_get_user_by_id.call_count == 1
    assert mock_get_transcriptions_by_user_id.call_count == 1
    assert mock_get_blob_name_from_url.call_count == 3
    assert mock_generate_sas_url.call_count == 3

    assert response.status_code == 200

    for idx, transcription_item in enumerate(response.json()["data"], start=1):
        assert transcription_item["transcription"] == f"Transcription text {idx}"


@patch("core.auth.verify_jwt_token")
def test_get_all_transcriptions_401(
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
        url="/transcription/all", headers={"Authorization": "Bearer invalid_token"}
    )

    assert mock_verify_jwt_token.call_count == 1
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


@patch("api.routes.transcription.get_user_by_id")
def test_get_all_transcriptions_404(
    mock_get_user_by_id: MagicMock, client_factory: TestClient
):
    client: TestClient = client_factory(
        sub=TEST_PAYLOAD["sub"], email=TEST_PAYLOAD["email"]
    )

    mock_get_user_by_id.return_value = None

    response = client.get(url="/transcription/all", headers=TEST_HEADERS)

    assert mock_get_user_by_id.call_count == 1
    assert response.status_code == 404
    assert response.json() == {"detail": "User's account not found"}
