# Coding Conventions and Rules for this Workspace

This document defines standard practices and constraints.

## 1. General Principles

- **Simplicity First**: Write readable, maintainable scripts for setup and database tests.
- **Explicit Logging**: Python scripts must output clear logs on execution steps, including SQL queries executed and results returned.

## 2. Docker & Database Standards

- **Named Volumes**: Docker volumes must be named explicitly to persist data (e.g., `postgresql-data`).
- **Connection Health Checks**: Always wait for PostgreSQL to be healthy before attempting database connections.
- **PostgreSQL Client Tools**: When writing python scripts to connect to PostgreSQL, use standard packages like `psycopg2-binary` or `sqlalchemy`.

## 3. Report Standards

- **Formatting**: The Word report (`.docx`) must contain clear sections, tables for SQL output where applicable, and placeholders for screenshots.
