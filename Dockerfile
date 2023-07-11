# Use an Ubuntu base image
FROM ubuntu:latest

# Install necessary packages for C++ development
RUN apt-get update && \
    apt-get install -y build-essential g++ cmake

# Set the working directory
WORKDIR /jacobs-ladder

# Copy the source code into the container
COPY . /jacobs-ladder

# Build the project using CMake
RUN mkdir build && \
    cd build

RUN cmake ./CMakeLists.txt && \
    make

# Uncomment if you want the container to stop after it is finished running
# CMD ["./build/Triads"]
