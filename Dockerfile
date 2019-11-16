FROM python:3

WORKDIR /app

RUN mkdir /storage/

COPY onlooker.py /app/

CMD [ "python", "./onlooker.py" ]