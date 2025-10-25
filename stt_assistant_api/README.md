### BE part

---

### Coding points

1. Implementation of <ins>SAS tokens</ins> for audio file URL accessibility:

```python
def generate_sas_url(blob_name: str, expiry_minutes: int = 5) -> str:
    sas_token = generate_blob_sas(
        account_name=az_settings.STORAGE_ACCOUNT_NAME,
        container_name=az_settings.STORAGE_BLOB_CONTAINER,
        blob_name=blob_name,
        account_key=az_settings.STORAGE_ACCOUNT_KEY,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes),
    )

    sas_url = (
        f"https://{az_settings.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/"
        f"{az_settings.STORAGE_BLOB_CONTAINER}/{blob_name}?{sas_token}"
    )

    return sas_url
```

2. Verification of audio uniqueness using <ins>UUID5</ins>:

```python
def get_deterministic_blob_name(filename: str, suffix: str) -> str:
    base_name = os.path.splitext(filename)[0]
    deterministic_uuid = uuid.uuid5(uuid.NAMESPACE_URL, base_name)

    return f"{deterministic_uuid}{suffix}"
```

3. Implementation of <ins>client factory fixture</ins>:

```python
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
```

---

### Improvements to consider

- Organize business logic in the following modules using classes:
  - _speech_service.py_
  - _storage_service.py_
- With regard to the verification of audio file uniqueness in Blob storage, use hashing of the audio file content

---
