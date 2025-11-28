# Tender Scraper - Development Charter

## Git & GitHub

- Use GitHub CLI (`gh`) for all GitHub operations
- Branch naming: prefix with `lmj/` (e.g., `lmj/feature-scraper`, `lmj/fix-gemini-api`)
- Commit messages: use conventional commits format (`feat:`, `fix:`, `docs:`, `refactor:`)
- Never force push to `main` branch

## Python

- Always run code in virtual environment (`.venv`)
- Python version: 3.10+
- Code style: follow PEP 8, use `black` for formatting, `ruff` for linting
- Type hints: mandatory for all functions
- Async first: prefer `async/await` for I/O operations

## Project Structure

- Keep modular architecture: `routers/`, `models/`, `services/`, `scrapers/`, `utils/`
- Separate concerns: scraping logic stays in `scrapers/`, AI logic in `services/ai/`
- Configuration: use environment variables, never hardcode credentials
- Database migrations: use Alembic, never manual schema changes

## API Development

- FastAPI: use dependency injection for database sessions
- Pydantic: define schemas for all request/response models
- Error handling: use custom exceptions, return meaningful error messages
- Documentation: auto-generated via FastAPI, keep docstrings minimal but clear

## Testing

- Write tests before marking features complete
- Coverage target: core modules > 80%
- Use `pytest` with async support
- Mock external APIs (Gemini, target websites)

## Dependencies

- Minimize dependencies, prefer standard library when possible
- Pin versions in `requirements.txt`
- Separate `requirements-dev.txt` for development tools

## AI/LLM Integration

- API Key: ALWAYS use `os.getenv("GEMINI_API_KEY")`, never hardcode
- Model: use `gemini-3-pro-preview` for all tasks
- Client initialization: create singleton instance at module level
- System instructions: define via `systemInstruction` in config, not in user prompt
- Temperature: use 0.4-0.7 for structured extraction (lower = more deterministic)
- Output parsing: implement robust regex extraction for JSON/structured data
- Error handling: wrap all API calls in try-catch, log errors without exposing API keys
- Retry logic: exponential backoff with max 3 attempts
- Response validation: always validate with Pydantic before saving to database
- Token optimization: strip HTML noise before sending (HTML → Markdown)

## Database

- PostgreSQL only
- Use indexes for frequently queried fields
- JSONB for raw/unstructured data, relational for structured
- Never delete data, use soft delete (status flags)

## Documentation

- Code is self-documenting, avoid redundant comments
- Update docs/ only when architecture changes
- README: keep concise with setup instructions only
- No changelog files, use git history
- After completing phase tasks: update `docs/task.md` status and suggest next tasks

## Security

- Environment variables for all secrets (`.env`, never committed)
- Sanitize HTML before processing
- Validate all external inputs with Pydantic
- Rate limiting on API endpoints

## Performance

- Use async wherever possible (httpx, asyncpg)
- Implement caching with Redis for hot data
- Batch database operations
- Profile before optimizing

## Workflow

- Small, focused commits
- PR review required before merging to main
- Run tests locally before pushing
- Delete branches after merging
