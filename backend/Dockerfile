FROM python:3.7-buster

WORKDIR /app

ADD ./ /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]
