# Repository Guidelines

## Project Structure & Module Organization
- backend: FastAPI app (`main.py`), routers in `backend/api/`, business logic in `backend/services/`, Pydantic schemas in `backend/schemas/`, DB session/models/migrations in `backend/db/`, helpers in `backend/utils/`.
- frontend: React/Vite app under `frontend/` with pages in `frontend/src/pages/`, shared UI in `frontend/src/components/`, API client in `frontend/src/api/`.
- docs: API and architecture notes in `docs/`.
- tooling: `docker-compose.yml` for local stack, `Makefile` with common tasks, `.env.example` for configuration.

## Build, Test, and Development Commands
- `make up`: build and start DB, backend, and frontend (detached).
- `make logs` | `make ps`: stream logs or list containers.
- `make backend` | `make frontend`: open a shell inside the running service.
- `make migrate` | `make revision`: apply or generate Alembic migrations.
- `make seed`: load sample data via `backend/db/seeds.py`.
- Frontend: `cd frontend && npm run dev|build|preview`.
- Direct run: backend serves with `uvicorn main:app --reload` on port 8000.

## Coding Style & Naming Conventions
- Python: 4-space indent; modules/functions `snake_case`; classes `PascalCase`. Prefer FastAPI routers in `backend/api/*` delegating to `backend/services/*`.
- JS/React: components `PascalCase` (e.g., `Navbar.jsx`), files under `src/` grouped by feature (pages/components/api).
- Imports: prefer absolute within each app (e.g., `from services.ingest import ...`).
- Formatting: use `black` and `ruff` for Python, Prettier for JS (if configured). Keep functions small and pure in services.

## Testing Guidelines
- Python: prefer `pytest`; place tests in `backend/tests/` mirroring package paths. Aim for coverage of services and schemas.
- Frontend: prefer `@testing-library/react` and `vitest`; place tests next to components (`*.test.jsx`).
- Run: `pytest` in backend container; `npm test` (if added) in frontend.

## Commit & Pull Request Guidelines
- Commits: follow Conventional Commits seen in history (`feat:`, `fix:`, `docs:`, `chore:`); short imperative subject; optional emoji ok.
- PRs: include summary, scope (backend/frontend), steps to test, screenshots for UI, and linked issues. Keep PRs focused and small.

## Security & Configuration Tips
- Never commit secrets; copy `.env.example` to `.env`. Backend reads `DB_URL`/`DATABASE_URL`; adjust CORS for non-local origins. Enforce file upload limits and allowed extensions in upload API.

## AI Programming Agent (Codex)
- Primary Mission: Act as an expert programming assistant; deliver clean, efficient, secure, and understandable code that runs end‑to‑end.
- Core Principles: 
  - Clarity: descriptive names, simple designs over complexity.
  - Complete Solutions: include imports, minimal config, and a runnable example.
  - Rigorous Documentation: comment nontrivial logic; add a clear explanation and usage notes.
  - Security: never include secrets; use placeholders (e.g., `YOUR_API_KEY_HERE`); validate/sanitize inputs; prevent injections.
  - Best Practices: follow language/framework conventions; apply suitable patterns; keep code modular and reusable.
- User Interaction Flow: analyze the request; ask clarifying questions (language, framework, expected I/O) when ambiguous; generate the solution per principles; mentally test for logic/syntax/security issues; explain how to run and integrate (include install steps if needed).
- What to Avoid: assumptions about user knowledge; unnecessary complexity or “magic”; unreviewed or non‑runnable code; ignoring stated version/constraint requirements.
