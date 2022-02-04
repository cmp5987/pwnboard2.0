FROM python:3.9.10

COPY ./api-requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

