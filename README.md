# MineOps AI

An industrial maintenance intelligence platform in early development. The current
implementation is a FastAPI backend for browsing sample mining equipment; AI
capabilities and a frontend are not implemented yet.

## Current capabilities

- Health-check endpoint.
- List equipment and retrieve an asset by its numeric ID.
- Typed equipment responses validated with Pydantic.
- Automated API tests using pytest and FastAPI's test client.

Equipment is stored in an in-memory list containing two sample assets: a
Caterpillar haul truck and a Grundfos water pump. There is no database,
authentication, or equipment create/update/delete API.

## Tech stack

- **API:** Python, FastAPI, Uvicorn
- **Response schemas:** Pydantic
- **Tests:** pytest, HTTPX

Dependencies are pinned in [backend/requirements.txt](backend/requirements.txt).

## Getting started

You need Python 3 with `pip` and `venv`, and Git to clone the repository.
The code uses Python 3.10+ syntax; your interpreter must also support the pinned
dependencies.

```bash
git clone https://github.com/saurabhsinghnz/mineops-ai.git
cd mineops-ai/backend

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

python -m uvicorn app.main:app --reload
```

On Windows PowerShell, activate the environment with
`.venv\Scripts\Activate.ps1` instead.

Run the server from the `backend` directory so Python can resolve the `app`
package. No environment variables, database, or external AI service are required
for the current implementation.

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

## API

| Method | Endpoint                           | Description                                                     |
| ------ | ---------------------------------- | --------------------------------------------------------------- |
| `GET`  | `/health`                          | Returns `{"status": "ok"}`.                                     |
| `GET`  | `/api/v1/equipment`                | Returns an array of all equipment records.                      |
| `GET`  | `/api/v1/equipment/{equipment_id}` | Returns one equipment record, or HTTP 404 if it does not exist. |

### Examples

With the server running:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/v1/equipment
curl http://127.0.0.1:8000/api/v1/equipment/1
```

The single-equipment endpoint returns:

```json
{
  "id": 1,
  "asset_code": "HT-102",
  "name": "Haul Truck 102",
  "equipment_type": "Haul Truck",
  "site": "Site A",
  "manufacturer": "Caterpillar",
  "model": "793F"
}
```

An unknown ID returns HTTP 404 with:

```json
{
  "detail": "Equipment not found"
}
```

## Running tests

From `backend`, with the virtual environment activated and dependencies installed:

```bash
pytest -v
```

The tests cover the health check, equipment listing, an empty equipment list,
retrieval by ID, and an unknown ID. [backend/pytest.ini](backend/pytest.ini)
sets the Python import path for test discovery.

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
    api/equipment.py              # Equipment HTTP routes
    schemas/equipment.py          # Equipment response schema
    services/equipment_service.py # Sample data and lookup functions
  tests/test_equipment.py         # API tests
  pytest.ini                     # Test configuration
  requirements.txt               # Pinned runtime and test dependencies
```
