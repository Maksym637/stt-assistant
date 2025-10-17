# stt-assistant
STT-Assistant web app with BE and FE parts that transcribes audio into editable text
- - -
### Project description
TODO
- - -
### Services configuration
1. Azure `Speech` Service:
```json
{
    "Region": "<YOUR RELEVANT REGION>",
    "API Kind": "SpeechServices",
    "Pricing tier": "Free"
}
```
2. Azure `Storage account` Service:
```json
{}
```
3. Azure `Database for PostgreSQL` Service:
```json
{}
```
- - -
### Interesting coding points
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
# TODO
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
- - -
### Improvements to consider
1. Organize business logic in the following modules using classes:
    - `/services/speech_service.py`
    - `/services/storage_service.py`
2. With regard to the verification of audio file uniqueness in Blob storage, use hashing of the audio file content
- - -
### Project execution
#### Prerequisites:
Before executing the project, fill in the following files in the `env` folder:
- `.api.env`:
```ini
ENV=

AUTH0_DOMAIN=
AUTH0_AUDIENCE=
```

- `.azure.env`:
```ini
SPEECH_KEY=
SPEECH_REGION=

STORAGE_CONNECTION_STRING=
STORAGE_ACCOUNT_NAME=
STORAGE_ACCOUNT_KEY=
STORAGE_BLOB_CONTAINER=

DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_NAME=
```

- `.env.client`:
```ini
VITE_AUTH0_DOMAIN=
VITE_AUTH0_CLIENT_ID=
VITE_AUTH0_AUDIENCE=
```

#### BE execution:
1. Go to the `stt_assistant_api` dir
2. Install all dependencies using the command below:
```bash
poetry install
```
3. Activate poetry using the command below:
```bash
poetry env list --full-path
```
```bash
source [poetry env path]/bin/activate
```
4. Launch the BE part using the command below:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### FE execution:
TODO
- - -
### Tests execution
To execute tests, follow these steps:
1. Install all dependencies and activate poetry as described earlier in the `BE execution` section
2. Execute tests with coverage using the command below:
```bash
PYTHONPATH=. pytest --cov
```
- - -
### Demonstration
TODO
- - -
