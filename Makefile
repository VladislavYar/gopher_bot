makemigrations: # Создание миграций
	python src/manage.py makemigrations

migrate: # Выполнение миграций
	python src/manage.py migrate

collectstatic: # Собрать статику.
	python src/manage.py collectstatic --noinput

createsuperuser: # Создать супер пользователя.
	python src/manage.py createsuperuser --noinput

project-start-local: # Запуск проекта local.
	make migrate;
	make collectstatic;
	cd src && uvicorn config.asgi:application --lifespan=on --reload;

project-init-local: # Инициализация проекта local.
	make migrate;
	make createsuperuser;
	make collectstatic;
	cd src && uvicorn config.asgi:application --lifespan=on --reload;
