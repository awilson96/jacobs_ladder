cmake_minimum_required(VERSION 3.10)
project(Triads)

set(CMAKE_CXX_STANDARD 20)

# Set the output directory
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/build)

# Add the executable target for Triads.cpp
add_executable(Triads
    src/Triads.cpp
)

# Add the necessary dependencies
target_include_directories(Triads PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
)

# Set up the dependencies
target_sources(Triads PRIVATE
    src/Intervals.h
    src/Notes.h
)