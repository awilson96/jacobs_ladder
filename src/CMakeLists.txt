cmake_minimum_required(VERSION 3.10)
project(Jacobs-Ladder)

set(CMAKE_CXX_STANDARD 11)

# Add your source files here
set(SOURCES
    Triads.cpp
)

# Add your header files here
set(HEADERS
    Intervals.h
    Notes.h
    Triads.h
)

# Add the executable target
add_executable(my_executable ${SOURCES} ${HEADERS})
