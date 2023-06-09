build:
	@ docker compose build

down:
	@ docker compose down

up: build migrate
	@ docker compose up -d

migrate: build
	@ docker compose run --rm tks-technical-test-api python main.py migrate

deps:
	@ docker compose run --rm tks-technical-test-api poetry install

bash:
	@ docker compose run --rm tks-technical-test-api /bin/sh

test:
	@ docker compose run --rm tks-technical-test-api python -m unittest

coverage: build migrate
	@ docker compose run --rm skeleton-py-flask-api /bin/ash -c "coverage run --source='api' --omit='api/tests/*' -m unittest"
	@ docker compose run --rm skeleton-py-flask-api coverage report
	@ docker compose run --rm skeleton-py-flask-api coverage xml
	@ docker compose run --rm skeleton-py-flask-api coverage html
