FROM tiangolo/meinheld-gunicorn-flask:python3.7

WORKDIR /app

RUN apt update -y && apt upgrade -y
RUN apt install cmake -y
COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN apt autoremove cmake -y
RUN mkdir /app/images/

COPY ./ ./

