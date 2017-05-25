FROM ubuntu:latest
MAINTAINER Santiago Suarez Ordonez "santiycr@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app/web
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
