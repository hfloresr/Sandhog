NAME    = malmopy-cntk-cpu-py27
TAG     = latest
LIB     = ./lib/malmo-challenge/docker
DIR     = ./docker
EXPDIR  = sandhog
EXP     = sandhog_experiment

default: images

images:
	docker build $(LIB)/malmo -t malmo:$(TAG)
	docker build $(DIR)/$(NAME) -t $(NAME):$(TAG)

experiment:
	docker build $(EXPDIR) -t $(EXP):$(TAG)
	docker-compose -f $(DIR)/$(EXPDIR)/docker-compose.yml up

.PHONY: build clean
