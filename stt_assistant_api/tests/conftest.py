import pytest

from fastapi.testclient import TestClient

from core.auth import get_current_account

from schemas.auth import Auth0Payload

from main import app


@pytest.fixture
def client_factory():
    def make_client(sub: str, email: str, is_authenticated=True):
        if not is_authenticated:
            return TestClient(app)

        app.dependency_overrides[get_current_account] = lambda: Auth0Payload(
            sub=sub, email=email
        )
        client = TestClient(app)

        return client

    yield make_client

    app.dependency_overrides.clear()
