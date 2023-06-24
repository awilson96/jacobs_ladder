cmake_minimum_required(VERSION 3.10)
project(JacobsLadder)

set(CMAKE_CXX_STANDARD 11)

# Specify the order of compilation
set(SOURCES
    src/Notes.h
    src/Intervals.h
    src/Triads.h
    src/Triads.cpp
)

# Add the executable target
add_executable(my_executable ${SOURCES})
