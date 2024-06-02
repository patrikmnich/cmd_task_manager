FROM python:3.12

WORKDIR /app
COPY . /app

ADD requirements.txt .
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]