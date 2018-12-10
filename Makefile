default:
	echo Hello There

publish:
	docker build -t publish:unity -f publish.Dockerfile .
	docker run --rm -v `pwd`:/code -it publish:unity sh

unity:
	# docker build -t build:unity -f unity.Dockerfile .
	docker run --rm -v `pwd`:/code -w /code -it build:unity sh