FROM python:3.9

ENV PYTHONUNBUFFERED=1
ENV C_FORCE_ROOT=1
ENV FLASKDIR=/app

RUN mkdir ${FLASKDIR}
WORKDIR ${FLASKDIR}

COPY requirements.txt ${FLASKDIR}
RUN pip install -r requirements.txt

COPY . ${FLASKDIR}
