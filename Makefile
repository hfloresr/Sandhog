NAME    = malmopy-cntk-cpu-py27
TAG     = latest
LIB     = ./lib/malmo-challenge/docker
DIR     = ./docker
SANDIR  = sandhog
SAND    = sandhog_experiment
RANDIR  = random
RAND    = random_experiment
ADIR    = astar
ASTAR   = astar_experiment
DQN     = dqn_experiment
DQNDIR  = dqn


default: images

images:
	docker build $(LIB)/malmo -t malmo:$(TAG)
	docker build $(DIR)/$(NAME) -t $(NAME):$(TAG)

sandstar:
	docker build $(SANDIR) -t $(SAND):$(TAG)
	docker-compose -f $(DIR)/$(SANDIR)/docker-compose.yml up

astar:
	docker build $(SANDIR) -t $(ASTAR):$(TAG)
	docker-compose -f $(DIR)/$(ADIR)/docker-compose.yml up

random:
	docker build $(SANDIR) -t $(RAND):$(TAG)
	docker-compose -f $(DIR)/$(RANDIR)/docker-compose.yml up

dqn:
	docker build $(SANDIR) -t $(DQN):$(TAG)
	docker-compose -f $(DIR)/$(DQNDIR)/docker-compose.yml up



.PHONY: build clean
