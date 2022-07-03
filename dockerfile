FROM docker.io/python:3.8
#FROM python:3.8-slim-buster
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY ./app.py /app
CMD [ "python", "index.py" ]
#ENTRYPOINT [ "python" ]
#CMD [ "app.py" ]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" ]
