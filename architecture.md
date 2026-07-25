# Project Architecture: PostgreSQL and Label Studio Integration

This document maps out the system architecture and data flows for the PostgreSQL and Label Studio integration.

## 1. Directory Structure

```text
├── backend/                  # Core backend Python workspace member
│   ├── core/                 # Shared core settings and configs
│   ├── sandbox/              # Sandbox test scripts and legacy Assignment 1 scripts
│   │   ├── db_test_assignment1.py         # Assignment 1 PostgreSQL CRUD test script
│   │   ├── report_generator_assignment1.py # Assignment 1 Word report generator script
│   │   └── test_settings.py  # Script to verify settings configuration
│   ├── enqueue.py            # Script to enqueue background tasks to Redis
│   ├── generate_report.py    # Script to automate generation of Word report for Assignment 3
│   ├── label_studio_test.py  # Script to test Label Studio SDK integration
│   ├── postgres_test.py      # Script to test PostgreSQL CRUD operations
│   ├── worker_settings.py    # ARQ background worker configuration
│   └── ...
├── overview/                 # System architecture overview diagrams
│   ├── overview.drawio       # Draw.io source architecture diagram
│   └── overview.png          # Rendered PNG of system architecture diagram
├── storage/                  # Workspace file and database storage
│   ├── artifacts/            # Output documents, reports (PDF & DOCX), and screenshots
│   │   ├── 6710110589.pdf                       # Submission report PDF (Assignment 1)
│   │   ├── Assignment1_Submission_Checklist.docx  # Final Word report (Assignment 1)
│   │   └── README.md
│   ├── data/                 # Data cache and persistence directory
│   └── log/                  # System and Docker log storage
├── utils/                    # Shared utility functions and scripts
├── compose.yml               # Docker Compose configuration (Redis, PostgreSQL, Label Studio)
├── task-graph.md             # Living roadmap and execution blueprint
├── architecture.md           # Architecture definition and data flows
└── skill-instructions.md     # Coding standards and guidelines for this workspace
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
