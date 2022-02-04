FROM python:3.9.10

COPY ../docker/api-requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

