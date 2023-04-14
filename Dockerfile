FROM alpine:latest

ENV DEBIAN_FRONTEND="noninteractive" TZ="Europe/Paris"

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

RUN apk add gcc
RUN apk add 
RUN apk add libgphoto2-dev \
    apache2 \
    curl \
    git \ 
    python3-dev \ 
    linux-headers  \
    musl-dev

     
COPY ./ /carlab-shoot/

WORKDIR /carlab-shoot/

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "sh" ]
CMD [ "launch.sh" ]