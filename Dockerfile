FROM python:3
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN cd django_project
CMD ["python","manage.py","runserver"]