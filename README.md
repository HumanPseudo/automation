# Automation Hub

A standard high-level Python project for automation, integrated as skills for Nanobot.

## Project Structure

- `src/automation_hub/`: Core logic and service integrations.
- `skills/`: Nanobot skill definitions. Each skill has a `SKILL.md` and associated scripts.
- `tests/`: Project tests.

## Setup

1.  **Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -e .
    ```

2.  **Configuration:**
    Copy `.env.example` to `.env` and fill in your API keys and credentials.

## Nanobot Integration

This project is designed to be compatible with [Nanobot](https://github.com/vllm-project/vllm). To use these skills, point Nanobot to the `skills/` directory.

### Available Skills

- **Workspace**: Automation for Google Workspace (Docs, Sheets, Calendar).
- **Social Media**: Automated posting and interaction for social platforms.

## Development

- Add new service integrations in `src/automation_hub/services/`.
- Expose new functionalities as skills in the `skills/` directory.
