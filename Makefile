NAME = malmopy-cntk-cpu-py27
TAG = latest
DIR = ./lib/malmo-challenge/docker
EDIR = ./sandhog
ENAME = my_experiment

default: images

images:
	docker build $(DIR)/malmo -t malmo:$(TAG)
	docker build $(DIR)/$(NAME) -t $(NAME):$(TAG)

experiment:
	docker build $(EDIR) -t $(ENAME):$(TAG)
	docker-compose -f $(EDIR)/docker-compose.yml up

.PHONY: build clean
