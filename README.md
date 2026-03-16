# Incubyte Salary Management API

A FastAPI application implementing employee CRUD operations and salary calculations with country-based tax deductions.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| Database | SQLite + SQLAlchemy |
| Testing | pytest + httpx |
| Language | Python 3.10+ |

---

## How to Install and Run Locally

```bash
# 1. Clone the repository
git clone <repo-url>
cd incubyte-exercise

# 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.
Interactive docs: `http://localhost:8000/docs`

---

## How to Run Tests

```bash
pytest tests/ -v
```

Tests use an in-memory SQLite database — no setup required. Each test runs in full isolation.

---

## Full API Reference

### Employee CRUD

#### POST /employees — Create employee

**Request body:**
```json
{
  "full_name": "Alice Smith",
  "job_title": "Engineer",
  "country": "India",
  "salary": 75000.0
}
```

**Response `201`:**
```json
{
  "id": 1,
  "full_name": "Alice Smith",
  "job_title": "Engineer",
  "country": "India",
  "salary": 75000.0
}
```

Returns `422` if any field is missing or `salary` is not a positive number.

---

#### GET /employees/{id} — Get employee by ID

**Response `200`:**
```json
{
  "id": 1,
  "full_name": "Alice Smith",
  "job_title": "Engineer",
  "country": "India",
  "salary": 75000.0
}
```

Returns `404` if employee not found.

---

#### GET /employees — List all employees

**Response `200`:**
```json
[
  {
    "id": 1,
    "full_name": "Alice Smith",
    "job_title": "Engineer",
    "country": "India",
    "salary": 75000.0
  }
]
```

Returns empty array `[]` if no employees exist.

---

#### PUT /employees/{id} — Update employee

**Request body** (all fields optional):
```json
{
  "salary": 90000.0,
  "job_title": "Senior Engineer"
}
```

**Response `200`:** Updated employee object.
Returns `404` if employee not found.

---

#### DELETE /employees/{id} — Delete employee

**Response `200`:**
```json
{
  "message": "Employee with id 1 deleted successfully"
}
```

Returns `404` if employee not found.

---

### Salary Calculation

#### GET /employees/{id}/salary — Calculate net salary

**Response `200`:**

India (TDS = 10%):
```json
{
  "gross_salary": 100000.0,
  "deductions": { "tds": 10000.0 },
  "net_salary": 90000.0
}
```

United States (TDS = 12%):
```json
{
  "gross_salary": 100000.0,
  "deductions": { "tds": 12000.0 },
  "net_salary": 88000.0
}
```

Other countries (no deductions):
```json
{
  "gross_salary": 100000.0,
  "deductions": {},
  "net_salary": 100000.0
}
```

Returns `404` if employee not found.

---

### Salary Metrics

#### GET /salary/metrics — Salary metrics with filters

**Query params:** `country` and/or `job_title`

**Examples:**
- `GET /salary/metrics?country=India`
- `GET /salary/metrics?job_title=Engineer`

**Response `200`:**
```json
{
  "min_salary": 50000.0,
  "max_salary": 90000.0,
  "average_salary": 70000.0
}
```

Returns `404` with a descriptive message if no employees match the filter.

---

## Implementation Details

### AI Tools Used
**Claude Code by Anthropic** — AI-powered CLI for software development.

### How AI Was Used
- **Project scaffolding**: Generated the initial project structure, `requirements.txt`, `database.py`, `models.py`, FastAPI app skeleton, and `conftest.py` test fixtures
- **TDD workflow**: Drove the Red-Green-Commit cycle for all 12 features — writing failing tests first, then implementing the minimal code to pass them
- **Feature implementation**: Implemented all CRUD routes, salary calculation logic, and metrics endpoints
- **Git workflow**: Managed the granular commit history following the `test:` / `feat:` / `refactor:` convention throughout

### What Was Manually Reviewed
- All business logic verified against requirements (TDS rates, metrics calculations)
- Test coverage reviewed to ensure each happy path and error case is covered
- README written with human oversight to ensure accuracy
- Deduction rules (India 10%, US 12%, others 0%) confirmed against specification
