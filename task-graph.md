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

## Phase 6: Workspace Cleanup & Documentation Sync
- [x] **Task 6.1**: Rename directory `untils` to `utils`
    - *File*: [dir_utils.py](file:///c:/eco/friday/utils/dir_utils.py), [logging_utils.py](file:///c:/eco/friday/utils/logging_utils.py)
    - *Logic/Target*: Move `dir_utils.py` and `logging_utils.py` from `untils` to `utils` and remove empty `untils` directory.
    - *Why*: Fix the typo directory name `untils` to standard name `utils`.
    - *Verification*: **[AUTONOMOUS]** Run Powershell command to test path existence of `utils/` and non-existence of `untils/`.
- [x] **Task 6.2**: Delete empty/unused folders `frontend` and `worker` at workspace root
    - *File*: [frontend](file:///c:/eco/friday/frontend), [worker](file:///c:/eco/friday/worker)
    - *Logic/Target*: Remove the empty directories `frontend` and `worker` from the root workspace directory.
    - *Why*: Remove clutter and keep the workspace tidy.
    - *Verification*: **[AUTONOMOUS]** Run command to verify `frontend/` and `worker/` folders do not exist.
- [x] **Task 6.3**: Update README.md files
    - *File*: [README.md](file:///c:/eco/friday/README.md), [backend/README.md](file:///c:/eco/friday/backend/README.md), [storage/artifacts/README.md](file:///c:/eco/friday/storage/artifacts/README.md)
    - *Logic/Target*: Replace empty README files with comprehensive project and sub-module descriptions.
    - *Why*: Keep project documentation clear, clean, and helpful.
    - *Verification*: **[AUTONOMOUS]** Read README files and check their content length and formatting.
- [x] **Task 6.4**: Update architecture.md
    - *File*: [architecture.md](file:///c:/eco/friday/architecture.md)
    - *Logic/Target*: Update the directory structure ASCII tree and description to list the actual complete directory setup (`backend/`, `storage/`, `overview/`, `utils/`).
    - *Why*: Align architecture documentation with current actual workspace structure.
    - *Verification*: **[AUTONOMOUS]** View `architecture.md` and check the updated directory structure.

## Phase 7: Work1 Integration
- [x] **Task 7.1**: Move Docker Compose file to workspace root
    - *File*: [compose.yml](file:///c:/eco/friday/compose.yml)
    - *Logic/Target*: Move `work1/compose.yml` to root workspace.
    - *Why*: Centralize Docker configuration for the entire project workspace.
    - *Verification*: **[AUTONOMOUS]** Verify path existence of `compose.yml`.
- [x] **Task 7.2**: Move diagrams to `overview/`
    - *File*: [overview.drawio](file:///c:/eco/friday/overview/overview.drawio), [overview.png](file:///c:/eco/friday/overview/overview.png)
    - *Logic/Target*: Move `work1/diagrams/overview.drawio` and `overview.png` to `overview/`.
    - *Why*: Consolidate all system diagrams.
    - *Verification*: **[AUTONOMOUS]** Verify path existence of files in `overview/`.
- [x] **Task 7.3**: Move report artifacts to `storage/artifacts/`
    - *File*: [Assignment1_Submission_Checklist.docx](file:///c:/eco/friday/storage/artifacts/Assignment1_Submission_Checklist.docx), [6710110589.pdf](file:///c:/eco/friday/storage/artifacts/6710110589.pdf)
    - *Logic/Target*: Move document artifacts to `storage/artifacts/`.
    - *Why*: Store all output reports in a central storage area.
    - *Verification*: **[AUTONOMOUS]** Verify path existence of files in `storage/artifacts/`.
- [x] **Task 7.4**: Move Python scripts to `backend/sandbox/`
    - *File*: [db_test_assignment1.py](file:///c:/eco/friday/backend/sandbox/db_test_assignment1.py), [report_generator_assignment1.py](file:///c:/eco/friday/backend/sandbox/report_generator_assignment1.py)
    - *Logic/Target*: Move `work1/db_test.py` to `backend/sandbox/db_test_assignment1.py` and `work1/report_generator.py` to `backend/sandbox/report_generator_assignment1.py`.
    - *Why*: Prevent pollution of Assignment 3 backend directory, while preserving the previous work's sandbox scripts.
    - *Verification*: **[AUTONOMOUS]** Run `uv run python backend/sandbox/db_test_assignment1.py` to verify it compiles and runs.
- [x] **Task 7.5**: Cleanup redundant `work1` directory and local files
    - *File*: [work1](file:///c:/eco/friday/work1)
    - *Logic/Target*: Delete shortcut, readme, and the empty directory `work1`.
    - *Why*: Delete the messy folder and keep the main workspace clean.
    - *Verification*: **[AUTONOMOUS]** Verify `work1/` does not exist.
- [x] **Task 7.6**: Update root README.md and architecture.md
    - *File*: [README.md](file:///c:/eco/friday/README.md), [architecture.md](file:///c:/eco/friday/architecture.md)
    - *Logic/Target*: Add details about Assignment 1 components and update the ASCII directory tree.
    - *Why*: Align documentation with the new integrated project structure.
    - *Verification*: **[AUTONOMOUS]** View files and check updated contents.
