default:
	echo Hello There

publish:
	docker build -t publish:unity -f publish.Dockerfile .
	docker run --rm -v `pwd`:/code -it publish:unity sh

unity:
	# docker build -t build:unity -f unity.Dockerfile .
	docker run --rm -v `pwd`:/code -w /code -it build:unity sh

server:
	docker run --rm -p 8000:8000 -v `pwd`:/code -w /code/GameServer -it puzzle/server bash

build-server:
	docker build -t puzzle/server GameServer

joystick:
	docker run --rm -p 3000:3000 -v `pwd`:/code -w /code/joystickServer/StaticServer -it node:10-alpine npm start