FROM ubuntu

# updating base image and python/pip installation
RUN apt update
RUN apt install --yes python pip

# setting working directory
WORKDIR /opt/ui

# requirements file copying and all dependencies installation
COPY requirements.txt ./
RUN pip install -r requirements.txt

# rest project files copying
COPY ./ ./

# setting 8000 port
EXPOSE 7000
