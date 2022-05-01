# pwnboard2.0

## Starting the backend

In a shell run:
`mongod`
In a seperate shell run:
`python3 ./api/api.py`

## Starting the UI

In a shell cd into ui:
`npm install`

Then start the app by running:
`npm start`

## Start backend container manually.
`docker build -f .\dev.Dockerfile -t pwnboard-backend ..; docker run -p 5000:5000 --mount type=bind,source=C:\Users\cmpog\Desktop\projects\pwnboard2.0\,target=/app --name pwnboard-backend --rm -it pwnboard-backend /bin/sh -c 'mongod &>/dev/null & cd /app; python3 ./api/api.py'`