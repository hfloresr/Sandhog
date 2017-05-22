FROM microsoft/cntk:2.0.rc2-cpu-python2.7

# Version variables
ENV MALMO_VERSION 0.21.0
ENV MALMOPY_VERSION 0.1.0

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    ssh \
    git-all \
    zlib1g-dev \
    python-dev \
    python-pip \

    # install Malmo dependencies
    libpython2.7 \
    openjdk-7-jdk \
    lua5.1 \
    libxerces-c3.1 \
    liblua5.1-0-dev \
    libav-tools \
    python-tk \
    python-imaging-tk \
    wget \
    unzip && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Set CNTK Python PATH at first position to be picked automatically
ENV PATH=/root/anaconda3/envs/cntk-py27/bin:$PATH

# Update pip
RUN /root/anaconda3/envs/cntk-py27/bin/pip install --upgrade pip

# download and unpack Malmo
WORKDIR /root
RUN wget https://github.com/Microsoft/malmo/releases/download/$MALMO_VERSION/Malmo-$MALMO_VERSION-Linux-Ubuntu-16.04-64bit_withBoost.zip && \
    unzip Malmo-$MALMO_VERSION-Linux-Ubuntu-16.04-64bit_withBoost.zip && \
    rm Malmo-$MALMO_VERSION-Linux-Ubuntu-16.04-64bit_withBoost.zip && \
    mv Malmo-$MALMO_VERSION-Linux-Ubuntu-16.04-64bit_withBoost Malmo

ENV MALMO_XSD_PATH /root/Malmo/Schemas
ENV PYTHONPATH /root/Malmo/Python_Examples

# add and install malmopy, malmo challenge task and samples
WORKDIR /root
RUN git clone https://github.com/Microsoft/malmo-challenge.git && \
    cd malmo-challenge
WORKDIR /root/malmo-challenge
RUN pip install -e '.[all]'
