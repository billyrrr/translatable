FROM python:3.7

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS "./key.json"
#EXPOSE 8000
CMD gunicorn -b :8003 main:app
