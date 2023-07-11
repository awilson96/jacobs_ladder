# Use an Ubuntu base image
FROM ubuntu:latest

# Install necessary packages for C++ development
RUN apt-get update && \
    apt-get install -y build-essential g++ cmake curl

# Set the working directory
WORKDIR /jacobs-ladder

# Copy the source code into the container
COPY . /jacobs-ladder

# Add Catch2 library
RUN mkdir -p /jacobs-ladder/vendor/catch2 && \
    curl -L https://github.com/catchorg/Catch2/releases/download/v2.13.7/catch.hpp -o /jacobs-ladder/vendor/catch2/catch.hpp

# Build the project using CMake
RUN mkdir build && \
    cmake ./src && \
    make

# Uncomment if you want the container to stop after it is finished running
# CMD ["./build/Triads"]
