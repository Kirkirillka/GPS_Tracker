FROM python:3 as build-stage

ADD requirements.txt .
RUN pip install -r requirements.txt

FROM build-stage as preparation-stage
ENV PYTHONPATH "${PYTONPATH}:/app"


FROM preparation-stage as final-stage
WORKDIR /app