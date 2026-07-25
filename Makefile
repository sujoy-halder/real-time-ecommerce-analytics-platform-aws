.PHONY: test producer docker-up bootstrap

test:
	python scripts/run_tests.py

producer:
	cd services/event-producer && python -m app.main

docker-up:
	docker compose up --build

bootstrap:
	python scripts/bootstrap_localstack.py
