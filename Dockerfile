FROM python:latest
RUN mkdir /opt/app
WORKDIR /opt/app
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python","./app.py"]
