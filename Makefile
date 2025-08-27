# Marketing Analytics - Makefile

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

backend:
	docker compose exec backend bash

frontend:
	docker compose exec frontend bash

db:
	docker compose exec db psql -U app -d marketing

migrate:
	docker compose exec backend alembic upgrade head

revision:
	docker compose exec backend alembic revision --autogenerate -m "auto migration"

seed:
	docker compose exec backend python -m db.seeds
