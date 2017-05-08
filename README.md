# Sandhog


## Prerequisites

Install docker on your local machine by following the installation instructions for 
[Windows](https://docs.docker.com/docker-for-windows/install/), 
[Linux](https://docs.docker.com/engine/installation/), 
[MacOS](https://docs.docker.com/docker-for-mac/install/).


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
