FROM mongo

RUN apt update && apt install -y python3 python3-pip git curl
COPY ../docker/api-requirements.txt ./requirements.txt
RUN pip3 install -r ./requirements.txt

RUN curl -sL https://deb.nodesource.com/setup_16.x | bash
RUN apt install -y nodejs
