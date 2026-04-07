# Automation Hub

A modular and extensible framework for AI agent automation, providing high-level service integrations and persistent state management.

## Project Structure

- `src/automation_hub/`: Core logic, database models, and service integrations.
- `skills/`: Standardized skill definitions for AI agents. Each skill includes a `SKILL.md` and executable scripts.
- `tests/`: Comprehensive test suite.
- `alembic/`: Database migrations for persistent storage.

## Setup

1.  **Environment:**
    ```bash
    pipenv install --dev
    pipenv shell
    ```

2.  **Configuration:**
    Copy `.env.example` to `.env` and fill in your database credentials and API keys.

3.  **Database Migrations:**
    Initialize the database schema for persistent logging:
    ```bash
    alembic upgrade head
    ```

## Features

- **Agent-Ready Skills:** Pre-defined capabilities for AI agents to interact with third-party services.
- **Google Workspace Integration:** Advanced support for Calendar, Sheets, and Tasks using service accounts and dynamic ID management.
- **Database Infrastructure:** SQLAlchemy and PostgreSQL (via `psycopg2-binary`) for activity logging and persistent agent memory.
- **Automated Migrations:** Managed via Alembic for versioned schema changes.

## Agent Integration

This project is designed to be consumed by any AI agent or framework. To integrate these capabilities, point your agent to the `skills/` directory. Each skill follows a standardized format to describe its capabilities and requirements.

### Available Skills

- **Workspace**: Automation for Google Workspace (Docs, Sheets, Calendar).
- **Social Media**: Automated posting and interaction for social platforms.

## Development

- Add new service integrations in `src/automation_hub/services/`.
- Define database models in `src/automation_hub/core/models.py`.
- Expose new functionalities as skills in the `skills/` directory.
