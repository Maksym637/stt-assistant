# stt-assistant

STT-Assistant web app with BE and FE parts that transcribes audio into editable text

---

### Description

A full-stack web application that transcribes audio into editable text. The application consists of a front-end interface and a back-end server, providing seamless audio transcription and text editing capabilities. All user data and transcriptions are securily stored in an **Azure PostgreSQL Database**, while audio files are managed and stored in an **Azure Storage container**. For accurate and efficient transcription, the application leverages the **Azure Speech service**.

---

### Stack

- **Backend:** Python, FastAPI
- **Frontend:** JavaScript, React
- **Auth Services:** Auth0
- **Azure Services:** DB for PostgreSQL, Blob Storage, Speech Service

---

### Architecture

![stt-assistant-architecture](/docs/stt-assistant-architecture.png)

---

### DB Schema

![schema](/docs/schema.png)

**users**

Stores information about the user

| Column name | Type    | Description |
| ----------- | ------- | ----------- |
| id          | INT     | Primary key |
| auth0_id    | VARCHAR | Auth0 ID    |
| email       | VARCHAR | User email  |

**records**

Stores data related to recordings that are considered our audio files

| Column name | Type      | Description                   |
| ----------- | --------- | ----------------------------- |
| id          | INT       | Primary key                   |
| audio_url   | VARCHAR   | URL address of the audio file |
| created_at  | TIMESTAMP | Timestamp of record creation  |
| user_id     | INT       | User id                       |

**transcriptions**

Stores data related to user transcriptions

| Column name   | Type      | Description                         |
| ------------- | --------- | ----------------------------------- |
| id            | INT       | Primary key                         |
| transcription | VARCHAR   | Transcription text                  |
| language_code | VARCHAR   | Language code                       |
| created_at    | TIMESTAMP | Timestamp of transcription creation |
| record_id     | INT       | Record id                           |

---

### API Documentation

All API documentation can be found here - [API Redoc](https://maksym637.github.io/stt-assistant/docs/redoc.html) (\*All endpoints are Auth0 protected)

---

### App Execution

#### Prerequisites:

Before executing the project, fill in the following files in the `env` folder:

- `.api.env`:

```ini
ENV=

ORIGINS=

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

1. Go to the `stt_assistant_client` dir
2. Install all dependencies using the command below:

```bash
npm install
```

3. Launch the FE part using the command below:

```bash
npm run dev
```

---

### Tests execution

To execute tests, follow these steps:

1. Install all dependencies and activate poetry as described earlier in the `BE execution` section
2. Execute tests with coverage using the command below:

```bash
PYTHONPATH=. pytest --cov
```

---

### Demonstration

[Click here to see how application works](https://youtu.be/e-cuifbDaGA?si=rc-qnYLXkaEj2Dn0)

---
