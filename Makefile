run-api-server:
	clear
	python3 manage.py runserver

run-socket-server:
	clear
	python3 socketio_server.py

docker-clear:
	echo y|docker system prune --all

# docker-up