# Engineering log - 2026-11-02

## Scope and status

MineOps AI currently provides a small, read-only FastAPI backend for sample mining
equipment. It is an initial API foundation, not yet an AI-enabled maintenance
platform. There is no frontend implementation, database, authentication,
equipment write API, or AI integration.

### Application and API

- [Application entry point](../backend/app/main.py): creates the FastAPI app with
  title `MineOps AI` and version `0.1.0`, and registers the equipment router.
- `GET /health`: returns `{"status": "ok"}`. This is a basic application health
  response, not a check of databases or external services.
- [Equipment routes](../backend/app/api/equipment.py):
  - `GET /api/v1/equipment` returns all equipment as a JSON array.
  - An empty dataset returns HTTP 200 with `[]`.
  - `GET /api/v1/equipment/{equipment_id}` retrieves an asset by integer ID.
  - Missing assets return HTTP 404 with `{"detail": "Equipment not found"}`.
- FastAPI provides Swagger UI, ReDoc, and the OpenAPI schema using its default
  documentation endpoints.

### Data and response contract

- [EquipmentResponse](../backend/app/schemas/equipment.py) defines seven required
  fields: integer `id`, and string `asset_code`, `name`, `equipment_type`, `site`,
  `manufacturer`, and `model`.
- Both equipment routes declare response models, giving the API explicit output
  validation and generated schema documentation.
- [Equipment service](../backend/app/services/equipment_service.py) holds two
  sample assets.
- Listing returns the in-memory collection; retrieval performs a linear search
  and returns `None` when no asset matches. The HTTP layer translates that
  absence into a 404.

### Tests and developer setup

- [API tests](../backend/tests/test_equipment.py) use FastAPI's `TestClient` and
  cover five cases: health check, listing, empty listing, retrieval, and an
  unknown equipment ID.
- The [README](../README.md) documents virtual-environment setup, server startup,
  documentation URLs, request examples, and the `pytest -v` command.
- Local operation currently requires no database, environment variables, or
  external AI service.

## Technical decisions and trade-offs

The choices below are visible in the implementation. Their trade-offs are an
engineering assessment.

| Implemented choice                                            | Benefit                                                                                         | Trade-off / consequence                                                                                   |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Python with FastAPI and Uvicorn                               | Provides HTTP routing, parameter validation, and generated API documentation with little setup. | None                                                                                                      |
| Separate HTTP routes, response schemas, and service functions | Keeps transport concerns apart from data lookup and makes future changes easier to localize.    | Service results remain untyped dictionaries; there is no persistence boundary yet.                        |
| Versioned equipment routes under `/api/v1/equipment`          | Establishes an explicit API namespace from the start.                                           | Future contract changes will need a compatibility/versioning policy.                                      |
| Pydantic response models                                      | Establishes a consistent, validated equipment response shape.                                   | Domain constraints such as unique asset codes are not enforced by this schema.                            |
| In-memory sample data and read-only operations                | Allows the initial API to run without infrastructure or credentials.                            | Data is not durable, lookup is linear, and there is no production equipment management workflow.          |
| Synchronous route and service functions                       | Keeps the current non-I/O implementation straightforward.                                       | Database or external-service integration will require deliberate blocking/async handling.                 |
| Explicit 404 in the HTTP layer                                | Keeps HTTP error semantics out of the lookup service.                                           | None                                                                                                      |
| In-process API tests with a patched dataset                   | Exercises routing and serialization without starting a server.                                  | Does not validate deployment, real persistence, or external integrations.                                 |
| One fully pinned dependency file                              | Records exact dependency versions for installation.                                             | Runtime and development dependencies are mixed; an update and reproducibility workflow is not documented. |

## What can be improved

These are proposed follow-ups, not implemented features or approved commitments.

### Near-term foundation

1. **Strengthen API regression tests.** Assert full response fields and types,
   both sample assets, and the exact missing-asset error body. Add cases for
   non-integer IDs and define/test the intended behavior for zero and negative
   IDs. Do not equate five tests with complete contract coverage.
2. **Automate validation.** Add CI for the test suite, declare supported Python
   versions, and introduce consistent formatting, linting, and type checking.
   There is no tracked CI configuration or lint/type-check configuration yet.
3. **Improve service typing.** Add explicit return types and a typed internal
   equipment representation as the domain grows, while preserving the public
   response contract.
4. **Clarify dependency maintenance.** Separate runtime and test dependencies
   where useful, document how pins are updated, and verify clean-environment
   installation for the supported Python versions.

### Before real operational use

5. **Replace sample storage with persistence.** Select a database, add migrations
   and constraints, and make data access independently testable. Introduce the
   abstraction when persistence is needed rather than adding unused layers now.
6. **Define equipment management requirements.** Specify create/update/delete
   workflows, validation, asset-code uniqueness, pagination, filtering, and site
   scoping before expanding the API.
7. **Add access controls before exposing operational data.** Define
   authentication, authorization, and site-level data access requirements.
8. **Add operational visibility and deployment checks.** Introduce structured
   logging, request/error visibility, environment configuration, and a documented
   production startup process. Add readiness checks when real dependencies exist.

### Product direction

9. **Define an end-to-end maintenance use case.** Identify the first user
   workflow and required maintenance data before building the frontend or AI
   capabilities. Decide how AI output will be evaluated and reviewed rather than
   treating the project name as evidence that AI functionality exists.
