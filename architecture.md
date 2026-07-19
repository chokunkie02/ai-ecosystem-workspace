# Project Architecture: PostgreSQL and Label Studio Integration

This document maps out the system architecture and data flows for the PostgreSQL and Label Studio integration.

## 1. Directory Structure

```text
├── work1/
│   ├── compose.yml              # Docker Compose configuration (Redis, PostgreSQL, Label Studio)
│   ├── db_test.py               # Script to run CRUD tests on PostgreSQL
│   ├── report_generator.py      # Script to automate generation of Word report (.docx)
│   └── Assignment1_Submission_Checklist.docx  # Final Word report
├── task-graph.md            # Living roadmap and execution blueprint
├── architecture.md          # Architecture definition and data flows
└── skill-instructions.md    # Coding standards and guidelines for this workspace
```

## 2. Data Flow & System Design

```text
 [User Web Browser] <─── HTTP (Port 8080) ───> [Label Studio Container]
                                                        │
                                                        │ (Database Connection)
                                                        ▼
 [Docker postgresql-data Volume] <──────────> [PostgreSQL Container (Port 5432)]

 [Redis Container (Port 6379)] <───────────── [Docker redis-data Volume]
```

## 3. Component Details

- **Redis**: Container running official `redis:8.8.0-alpine` image. Exposes port `6379` locally.
- **PostgreSQL Database**: Container running official `postgres:15` image. Exposes port `5433` on the host, internally `5432`. Uses a persistent named volume `postgresql-data` for storage.
- **Label Studio**: Container running official `heartexlabs/label-studio:latest` image. Exposes port `8080`. Configured via environment variables to store its state and annotations in the PostgreSQL database.
- **Verification Scripts**: Local Python scripts to verify database operations and automate Word document generation.
