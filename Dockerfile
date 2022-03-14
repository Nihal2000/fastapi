# python base image in the container from Docker Hub
FROM python:3.7.9-slim

# copy files to the /app folder in the container
COPY ./app /app
COPY ./requirements.txt /requirements.txt
COPY ./detect /detect
COPY ./yolo_signature.pt /yolo_signature.pt

# RUN apt-get update && \
#     apt-get install -y \
#         build-essential \
#         python3-dev \
#         python3-setuptools \
#     && apt-get remove -y --purge build-essential \
#     && apt-get autoremove -y \
#     && rm -rf /var/lib/apt/lists/*

# set the working directory in the container to be /app
WORKDIR /

# install the packages from the Pipfile in the container
RUN python3 -m pip install -r requirements.txt

# expose the port that uvicorn will run the app on
ENV PORT=8000
EXPOSE 8000

# execute the command python main.py (in the WORKDIR) to start the app
CMD ["python", "app/main.py"]