IMAGE_NAME = ocr-image-reader
CONTAINER_NAME = ocr-container

.PHONY: all
all: build run

.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

.PHONY: run
run:
	docker run --name $(CONTAINER_NAME) $(IMAGE_NAME)

.PHONY: clean
clean:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker image prune -f

.PHONY: clean-all
clean-all:
	docker system prune -a -f

.PHONY: rebuild
rebuild: clean build run
