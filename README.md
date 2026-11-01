# Flask API Quality Starter

[![Python API tests](https://github.com/HamzaZahid172/simple-python-api/actions/workflows/ci.yml/badge.svg)](https://github.com/HamzaZahid172/simple-python-api/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?logo=flask)

A small Flask API that demonstrates **testable HTTP endpoints**, request validation, reliable status codes and a GitHub Actions test matrix. Suitable for learning API automation and submitting a first meaningful open-source pull request.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

API runs on **http://127.0.0.1:8000**. This demo uses an **in-memory store**, so data resets when the server restarts. It is not a production database or authentication service.

## API routes

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/` | API overview |
| GET | `/health` | Health check |
| GET | `/items` | List items |
| GET | `/items?category=course` | Filter items |
| GET | `/items?limit=2&offset=1` | Paginate items, with total matching count |
| GET | `/items/1` | Fetch one item or return 404 |
| DELETE | `/items/1` | Delete an item (204) or return 404 |
| POST | `/add-item` | Create item with JSON validation |

Example:

```bash
curl -X POST http://127.0.0.1:8000/add-item \
  -H 'Content-Type: application/json' \
  -d '{"name":"Integration tests","category":"project"}'
```

### Delete an item

```bash
curl -i -X DELETE http://127.0.0.1:8000/items/1
```

Deleting an existing item returns **204 No Content** with an empty response body.
Deleting a missing or previously deleted item returns **404** with an explanatory JSON
error. This demonstration stores items in memory: deletes reset on app restart.
New item IDs increase monotonically within the app instance, so deleting an item
does **not** cause its ID to be reused.

### Optional pagination

`GET /items` remains backward compatible when `limit` and `offset` are omitted.
To paginate, pass `limit` (1–100) and/or `offset` (a non-negative integer).
If only `offset` is provided, the default page size is 20. Filtering by
`category` happens **before** pagination.

```bash
curl 'http://127.0.0.1:8000/items?category=course&limit=1&offset=0'
```

A paginated response includes `items`, `count` (items in the current page),
`total` (all matching items), `offset` and `limit`. Invalid values return
**400** with an explanatory JSON error. This feature is useful for writing
API-client and pagination regression tests.

A successful create returns **201** and a JSON item with an ID. Invalid bodies return **400**; a non-JSON request returns **415**. Item `name` and `category` must be non-empty strings up to 100 characters.

## Tests and CI

```bash
python -m unittest discover -s tests -v
```

Tests verify health, listing/filtering, missing items, creates, malformed payloads, field validation and isolation between app instances. GitHub Actions runs this suite on Python **3.11 and 3.12** for pull requests and pushes to `main`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to propose a focused issue and submit a tested pull request. This is a learning project, and real code reviews are welcome.
