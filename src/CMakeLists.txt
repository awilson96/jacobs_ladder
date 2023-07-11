cmake_minimum_required(VERSION 3.10)
project(TriadsLib)

set(CMAKE_CXX_STANDARD 20)

# Set the output directory
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/build)

# Add the source files from the src directory as a library
add_library(TriadsLib STATIC
    Triads.cpp
    Intervals.h
    Notes.h
)

# Include the source directory as a target include directory
target_include_directories(TriadsLib PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

# Add the executable target for Triads.cpp
add_executable(Triads
    src/Triads.cpp
)

# Include the source directory as a target include directory
target_include_directories(TriadsLib PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

# Set the library output path
set_target_properties(TriadsLib PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/build
)
