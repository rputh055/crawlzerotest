# start from an official image
FROM ubuntu:20.04

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev && \
    apt-get install -y libpq-dev && \
    apt-get install -y wget


RUN python3 -m pip install --upgrade pip
RUN rm -f /usr/bin/python 
RUN ln -s /usr/bin/python3 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip 
    
# Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

RUN apt install -y ./google-chrome-stable_current_amd64.deb


#not changed

# Creating and putting configurations
RUN mkdir /config
ADD config/app /config/

# Installing all python dependencies
RUN pip install -r /config/requirements.txt
RUN mv /config/wait-for /bin/wait-for

# Open port 8000 to outside world
EXPOSE 8000

# When container starts, this script will be executed.
# Note that it is NOT executed during building
CMD ["sh", "/config/on-container-start.sh"]

# Creating and putting application inside container
# and setting it to working directory (meaning it is going to be default)
RUN mkdir /app
WORKDIR /app
ADD app /app/


