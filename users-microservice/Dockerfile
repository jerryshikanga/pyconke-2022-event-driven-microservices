#Create a ubuntu base image with python 3 installed.
FROM python:3.8-buster

# Set environment varibles
ENV PYTHONDONTWRITEBYTECDE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app

#Set the working directory
RUN mkdir /app
WORKDIR /app

# Install the dependencies
RUN apt-get -y update

# Install requirements
RUN pip install --upgrade pip==20.3.3
COPY requirements.txt .
RUN pip3 install -q -r requirements.txt

COPY . .

RUN chmod +x /app/db.sh
RUN /app/db.sh
