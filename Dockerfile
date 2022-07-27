FROM python:3

RUN apt-get update && apt-get install wget ca-certificates -y
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN cd django_project
ENTRYPOINT ["tail", "-f", "/dev/null"]