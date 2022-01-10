# getting base image python3.8
FROM python:3.8

#create work directory
WORKDIR /skyline

#copy file into image
COPY . /skyline

#install requirements
RUN pip3 install -r requirements.txt

#RUN the server
#CMD python3 skyline_algorithm/skyline_algorithm.py/
