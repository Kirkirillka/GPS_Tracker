FROM python:3.7 as build-stage

ADD requirements.txt .
RUN pip install -r requirements.txt

FROM build-stage as preparation-stage
ENV PYTHONPATH "${PYTONPATH}:/app"

# Install private packages
ADD dist dist
RUN pip install dist/*.whl


FROM preparation-stage as final-stage
WORKDIR /app