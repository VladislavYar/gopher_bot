makemigrations: # Создание миграций
	python src/manage.py makemigrations

migrate: # Выполнение миграций
	python src/manage.py migrate

collectstatic: # Собрать статику.
	python src/manage.py collectstatic --noinput

createsuperuser: # Создать супер пользователя.
	python src/manage.py createsuperuser --noinput

empty-makemigrations:
	python src/manage.py makemigrations --empty $(APP)

project-start-in-container: # Запуск проекта в контейнере.
	make migrate;
	make collectstatic;
	cd src && uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --lifespan=on;

clear-volumes-local: # Удаление Volumes.
	docker compose -f ./infra/docker-compose-local.yml --env-file ./infra/.env down --volumes;
	@sleep 5;

docker-compose-start-local: # Запуск контейнеров.
	docker compose -f ./infra/docker-compose-local.yml --env-file ./infra/.env up --no-deps -d;
	@sleep 5;

project-start-local: # Запуск проекта local.
	make docker-compose-start-local;
	make migrate;
	make collectstatic;
	cd src && uvicorn config.asgi:application --lifespan=on --reload;

project-init-local: # Инициализация проекта local.
	make clear-volumes-local;
	make docker-compose-start-local;
	make migrate;
	make createsuperuser;
	make collectstatic;
	cd src && uvicorn config.asgi:application --lifespan=on --reload;
