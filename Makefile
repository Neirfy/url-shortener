.PHONY: docker db run revision up test-db test

# Пути к файлам
ENV_DEV=.env
ENV_DEPLOY=.env.deploy
DOCKER_DEV=docker/docker-compose-dev.yml
DOCKER_DEPLOY=docker/docker-compose.yml
DOCKER_TEST=docker/docker-compose.test.yml

# --- Dev DB ---
db:
	@test -f $(DOCKER_DEV) || { echo "Error: $(DOCKER_DEV) not found"; exit 1; }
	@test -f $(ENV_DEV) || { echo "Error: $(ENV_DEV) not found"; exit 1; }
	docker-compose --env-file $(ENV_DEV) -f $(DOCKER_DEV) --project-directory . up --build -d

# --- Run app ---
run: db
	poetry run python src/main.py

# --- Deploy docker ---
docker: db
	@test -f $(DOCKER_DEPLOY) || { echo "Error: $(DOCKER_DEPLOY) not found"; exit 1; }
	@test -f $(ENV_DEPLOY) || { echo "Error: $(ENV_DEPLOY) not found"; exit 1; }
	docker-compose --env-file $(ENV_DEPLOY) -f $(DOCKER_DEPLOY) --project-directory . up --build -d

# --- Alembic migration ---
revision:
	poetry run alembic revision --autogenerate

up: revision
	poetry run alembic upgrade head


# --- Test DB ---
clean-test-db:
	@docker rm -f test_postgres 2>/dev/null || true
	docker-compose -f $(DOCKER_TEST) --project-directory . down --volumes --remove-orphans
	
test-db: clean-test-db
	@test -f $(DOCKER_TEST) || { echo "Error: $(DOCKER_TEST) not found"; exit 1; }
	docker-compose -f $(DOCKER_TEST) --project-directory . up -d --force-recreate --remove-orphans

test: test-db
	poetry run pytest -v