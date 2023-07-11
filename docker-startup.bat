@echo off

REM Build the Docker image
echo Building the Docker image...
docker build -t cpp-dev .

REM Run the Docker container
echo Running the Docker container...
docker run -it cpp-dev
