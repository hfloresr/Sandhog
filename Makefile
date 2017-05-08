NAME = malmopy-cntk-cpu-py27
TAG = latest
DIR = ./lib/malmo-challenge/docker

default: build

build:
	docker build $(DIR)/malmo -t malmo:$(TAG)
	docker build $(DIR)/$(NAME) - t $(NAME):$(TAG)

.PHONY: build clean
