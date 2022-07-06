FROM docker.io/python:3.8
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
CMD python app2.py
