From malmopy-cntk-cpu-py27:latest

RUN ["/bin/bash", "-c", "touch /etc/ld.so.conf.d/mpi.conf && echo '/root/openmpi/lib' >> /etc/ld.so.conf.d/mpi.conf && ldconfig && source ~/.bashrc"]

# Add experiments from local machine into docker image
ADD * /root/malmo-challenge/ai_challenge/pig_chase/
