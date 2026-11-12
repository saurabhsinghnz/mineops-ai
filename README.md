# MineOps AI

An industrial maintenance intelligence platform in early development. The current
implementation is a FastAPI backend for creating and browsing mining equipment
records; AI capabilities and a frontend are not implemented yet.

## Current capabilities

- Health-check endpoint.
- List equipment and retrieve an asset by its numeric ID.
- Create equipment records in a database.
- Typed equipment responses validated with Pydantic.
- Automated API tests using pytest and FastAPI's test client.

Authentication and equipment update/delete APIs are not implemented.

## Tech stack

- **API:** Python, FastAPI, Uvicorn
- **Database:** SQLAlchemy, Alembic
- **Response schemas:** Pydantic
- **Tests:** pytest, HTTPX

Dependencies are pinned in [backend/requirements.txt](backend/requirements.txt).

## Getting started

You need Python 3 with `pip` and `venv`, and Git to clone the repository.
The code requires Python 3.11 or newer; your interpreter must also support the pinned
dependencies.

```bash
git clone https://github.com/saurabhsinghnz/mineops-ai.git
cd mineops-ai/backend

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

# Example local database; alternatively, set DATABASE_URL in backend/.env.
export DATABASE_URL="sqlite:///./mineops.db"
alembic upgrade head
python -m uvicorn app.main:app --reload
```

On Windows PowerShell, activate the environment with
`.venv\Scripts\Activate.ps1` instead.

Run the server and migrations from the `backend` directory so Python can resolve
the `app` package. Set `DATABASE_URL` to a SQLAlchemy database URL in the
environment or in `backend/.env` before starting the application, and run the
migrations before using equipment endpoints. No external AI service is required.
In PowerShell, set the example URL with
`$env:DATABASE_URL = "sqlite:///./mineops.db"`.

The development server runs at http://127.0.0.1:8000:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- OpenAPI schema: http://127.0.0.1:8000/openapi.json

`--reload` is intended for local development.

### Database migrations

To generate schema changes run:

```bash
alembic revision --autogenerate -m "description"
```

To upgrade DB, run:

```bash
alembic upgrade head
```

To downgrade DB, run:

```bash
alembic downgrade base
```

Downgrading to `base` deletes the migrated tables and their data.

## API

| Method | Endpoint                           | Description                                                                                     |
| ------ | ---------------------------------- | ----------------------------------------------------------------------------------------------- |
| `GET`  | `/health`                          | Returns `{"status": "ok"}`.                                                                     |
| `GET`  | `/api/v1/equipment`                | Returns an array of all equipment records.                                                      |
| `GET`  | `/api/v1/equipment/{equipment_id}` | Returns one equipment record, or HTTP 404 if it does not exist.                                 |
| `POST` | `/api/v1/equipment`                | Creates a database record and returns it with HTTP 201, or HTTP 409 for a duplicate asset code. |

## Running tests

From `backend`, with the virtual environment activated, dependencies installed,
and `DATABASE_URL` set (as in the setup above):

The equipment tests use an isolated in-memory SQLite database. `DATABASE_URL`
is still required when the application is imported.

```bash
pytest -v
```

For coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

## Linting and formatting

To identify lint issues:

```bash
ruff check .
```

To format Python files:

```bash
ruff format .
```

Formatting fixes style inconsistencies; run `ruff check .` again to verify lint
issues. To apply automatic fixes for supported lint violations, run:

```bash
ruff check --fix .
```

## Project structure

```text
backend/
  app/
    main.py                       # FastAPI application and health check
    api/routes/equipment.py       # Equipment HTTP routes
    schemas/equipment.py          # Equipment request and response schemas
    services/service.py           # Database-backed equipment operations
  tests/test_equipment.py         # API tests
  pytest.ini                     # Test configuration
  requirements.txt               # Pinned runtime and test dependencies
```
