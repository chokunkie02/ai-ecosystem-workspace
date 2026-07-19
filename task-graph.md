# Assignment 3 Task Graph: Backend Setup & Services Integration (Work #1 - Work #5)

## Phase 1: Work #1 - Project Virtual Environment & Dependencies
- [x] **Task 1.1**: Initialize `uv` project inside `backend/` and create `.gitignore`
    - *File*: [pyproject.toml](file:///c:/eco/friday/backend/pyproject.toml), [.gitignore](file:///c:/eco/friday/backend/.gitignore)
    - *Logic/Target*: Run `uv init` in `backend` directory and create `.gitignore` to exclude `.venv/`, `__pycache__/`, `*.pyc`, `.env`.
    - *Why*: To create the isolated Python environment and manage project dependencies.
    - *Verification*: **[AUTONOMOUS]** Run `uv run python --version` and check `.gitignore` content.
- [x] **Task 1.2**: Install required packages using `uv add`
    - *File*: [pyproject.toml](file:///c:/eco/friday/backend/pyproject.toml), [uv.lock](file:///c:/eco/friday/backend/uv.lock)
    - *Logic/Target*: Run `uv add pydantic-settings arq sqlalchemy psycopg2-binary asyncpg label-studio-sdk python-dotenv` in `backend`.
    - *Why*: To install dependencies required for settings, ARQ, PostgreSQL, and Label Studio.
    - *Verification*: **[AUTONOMOUS]** Inspect `pyproject.toml` dependencies block.

## Phase 2: Work #2 - Project Settings
- [x] **Task 2.1**: Create `.env` file in `backend/`
    - *File*: [.env](file:///c:/eco/friday/backend/.env)
    - *Logic/Target*: Write Redis, Postgres, and Label Studio configurations.
    - *Why*: Centralize environment configuration for pydantic-settings.
    - *Verification*: **[AUTONOMOUS]** Verify `.env` file exists and contains expected keys.
- [x] **Task 2.2**: Create `core/config.py` with Settings class and `sandbox/test_settings.py`
    - *File*: [config.py](file:///c:/eco/friday/backend/core/config.py), [test_settings.py](file:///c:/eco/friday/backend/sandbox/test_settings.py)
    - *Logic/Target*: Implement `Settings(BaseSettings)` reading `.env` and test script to print `settings.model_dump()`.
    - *Why*: Validate Pydantic Settings configuration reading.
    - *Verification*: **[AUTONOMOUS]** Run `uv run python -m sandbox.test_settings` from `backend`.

## Phase 3: Work #3 - Redis + ARQ
- [x] **Task 3.1**: Create `worker_settings.py` and `enqueue.py`
    - *File*: [worker_settings.py](file:///c:/eco/friday/backend/worker_settings.py), [enqueue.py](file:///c:/eco/friday/backend/enqueue.py)
    - *Logic/Target*: Define `simple_work` and `WorkerSettings` in `worker_settings.py`, and `create_pool` job enqueuing in `enqueue.py`.
    - *Why*: Establish background task queue processing with ARQ & Redis.
    - *Verification*: **[AUTONOMOUS]** Run worker and test enqueue script against Redis.

## Phase 4: Work #4 - PostgreSQL CRUD
- [x] **Task 4.1**: Create `postgres_test.py`
    - *File*: [postgres_test.py](file:///c:/eco/friday/backend/postgres_test.py)
    - *Logic/Target*: Implement SQLAlchemy engine and CRUD operations (create_table, insert_data, update_data, delete_data, drop_table) for `students` table.
    - *Why*: Verify database connection and schema manipulation.
    - *Verification*: **[AUTONOMOUS]** Run `uv run python postgres_test.py` from `backend`.

## Phase 5: Work #5 - Label Studio SDK
- [x] **Task 5.1**: Create `label_studio_test.py`
    - *File*: [label_studio_test.py](file:///c:/eco/friday/backend/label_studio_test.py)
    - *Logic/Target*: Connect using `LabelStudio` client with API key from settings and list projects and tasks.
    - *Why*: Verify integration with Label Studio annotation service.
    - *Verification*: **[AUTONOMOUS]** Run `uv run python label_studio_test.py` from `backend`.
