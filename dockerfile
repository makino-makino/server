FROM python:3.7-alpine
RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY . /app/
CMD python3 app.py --host=0.0.0.0