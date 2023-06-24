# Use a Linux distribution as the base image
FROM ubuntu:latest

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    cmake

# Set the working directory
WORKDIR /cpp

# Copy the source code to the container
COPY . /cpp

# Run CMake to build the project
RUN mkdir build && cd build && cmake ..

# Build the project using make
RUN cd build && make

# Set the entry point to the built executable
ENTRYPOINT ["/cpp/build/triads"]
