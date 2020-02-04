FROM python:3

COPY src /app
WORKDIR /app

RUN pip install -r /app/requirements.txt

CMD [ "python", "/app/main.py" ]
