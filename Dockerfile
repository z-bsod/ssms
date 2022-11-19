FROM python:3
WORKDIR /app
ADD ./app/requirements.txt .
RUN pip install -r /app/requirements.txt
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install \
      monitoring-plugins \
      monitoring-plugins-contrib && \
    apt-get clean

RUN useradd monitoring -m

ADD ./app .
USER monitoring
