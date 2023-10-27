install:
	pip install -r requirements.txt --upgrade

migrate.up:
	alembic upgrade head

migrate.down:
	alembic downgrade -1

docker.up:
	docker-compose -f docker-compose.yaml up -d

docker.down:
	docker-compose -f docker-compose.yaml down -v

migrate.gen:
	alembic -x tenant=public revision --autogenerate

run.local:
	python main.py




