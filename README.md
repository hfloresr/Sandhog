# Sandhog


## Prerequisites

Install docker on your local machine by following the installation instructions for 
[Windows](https://docs.docker.com/docker-for-windows/install/), 
[MacOS](https://docs.docker.com/docker-for-mac/install/),
[Linux](https://docs.docker.com/engine/installation/).

To install docker for Ubuntu (replace xenial with your release, e.g. lsb_release -cs):
```
sudo apt-get update
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
sudo apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-xenial main'
sudo apt-get update
sudo apt-get install -y docker-engine
sudo usermod -aG docker $(whoami)
```


Install docker-compose by following the installation instructions (https://docs.docker.com/compose/install/)

Be sure to clone this repository recursively or manually to populate the malmo-challenge submodule
```
git clone --recursive https://github.com/hfloresr/Sandhog.git
```
or
```
git clone https://github.com/hfloresr/Sandhog.git
cd Sandhog
git submodule update --init --recursive
```


## Build the docker images

Build the required docker images:
```
make
```

Check to make sure that the images have been compiled:
```
docker images
```
You should see a list that includes the compiled images, e.g.,
```
REPOSITORY              TAG                          IMAGE ID            CREATED             SIZE
malmopy-cntk-cpu-py27   latest                       0161af81632d        29 minutes ago      5.62 GB
malmo                   latest                       1b67b8e2cfa8        41 minutes ago      1.04 GB
...
```

## Run the experiment

Run the challenge task with an example agent:
```
make experiment
```

The experiment is set up to start a tensorboard process alongside the experiment.
You can view it by pointing your browser to http://127.0.0.1:6006.
