docker-build:
	docker build . -f ./backend/docker/python/Dockerfile -t devalv/yawm-backend:0.4.0 -t devalv/yawm-backend:latest

docker-push:
	docker push devalv/yawm-backend:0.4.0
	docker push devalv/yawm-backend:latest

docker-tests:
	docker compose --env-file=backend/tests/.env -f docker-compose-test.yml up db-tests app-tests --build --force-recreate --abort-on-container-exit --exit-code-from app-tests

docker-up:
	docker compose --env-file=backend/.env up db app --build --force-recreate

test:
	cd backend && poetry run pytest

format:
	pre-commit run --all-files

coverage:
	cd backend && poetry run coverage run -m pytest
	cd backend && poetry run coverage html
