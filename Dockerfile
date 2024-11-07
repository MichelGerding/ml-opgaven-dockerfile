ARG processor=cpu

FROM nvidia/cuda:12.6.2-base-ubuntu24.04 AS build-gpu
LABEL authors="michel"

# install python
RUN apt-get update
RUN apt-get install -y python3-pip

ENV PIP_BREAK_SYSTEM_PACKAGES=1
RUN python3 -m pip install uv

# create and enable a venv
ENV VIRTUAL_ENV=/opt/venv
RUN uv venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN uv pip install tensorflow[and-cuda]


FROM ubuntu:24.04 AS build-cpu
LABEL authors="michel"

# install python
RUN apt-get update
RUN apt-get install -y python3-pip

WORKDIR /usr/ml-opgaven

ENV PIP_BREAK_SYSTEM_PACKAGES=1
RUN python3 -m pip install uv

ENV VIRTUAL_ENV=/opt/venv
RUN uv venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN uv pip install tensorflow


FROM build-${processor} AS final

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /usr/ml-opgaven

RUN uv pip install httpimport
RUN uv pip install jupyter

COPY requirements.txt /usr/ml-tmp/
RUN uv pip --no-cache-dir install -r /usr/ml-tmp/requirements.txt

COPY jupyter_extensions.txt /usr/ml-temp/
RUN uv pip install -r /usr/ml-temp/jupyter_extensions.txt \
    && rm -rf /tmp/ml-tmp

COPY opgaven/ .
EXPOSE 8888/tcp
CMD [ \
    "jupyter", "lab", \
    "--allow-root", \
    # listen to all incomming messages. The default is 127.0.0.1
    "--ip=0.0.0.0", \
    # dont try to open a browser window
    "--no-browser", \
    # Remove password requirement
    "--NotebookApp.token=''", \
    "--NotebookApp.password=''" \
]