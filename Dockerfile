# Use a Linux distribution as the base image
FROM ubuntu:latest

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    cmake

# Set the working directory
WORKDIR /src

# Copy the source code to the container
COPY . /src

# Build the C++ application
RUN cmake .
RUN make

# Set the entry point for the container
# CMD ["./your_application"]
