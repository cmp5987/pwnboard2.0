FROM mongo

RUN apt update && apt install -y python3 python3-pip git
COPY ../docker/api-requirements.txt ./requirements.txt
RUN pip3 install -r ./requirements.txt
