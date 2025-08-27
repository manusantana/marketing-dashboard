# Marketing Analytics - Makefile

up:
	docker compose up --build

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
