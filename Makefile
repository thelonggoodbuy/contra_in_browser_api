run-api-server:
	clear
	export DJANGO_ENV=local
	python3 manage.py runserver

run-socket-server:
	clear
	python3 socketio_server.py

docker-clear:
	echo y|docker system prune --all

# docker-up