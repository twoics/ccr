FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update && apk upgrade
RUN apk add --no-cache gcc g++ subversion musl-dev bash zlib-dev jpeg-dev python3-dev py3-numpy py3-pandas

ADD ./ /opt
WORKDIR /opt
RUN pip install -r requirements.txt
