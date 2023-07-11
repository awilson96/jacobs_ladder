cmake_minimum_required(VERSION 3.10)
project(TestTriads)

set(CMAKE_CXX_STANDARD 20)

# Add the executable target for TestTriads.cpp
add_executable(TestTriads
    TestTriads.cpp
)

# Include the Catch2 header file
target_include_directories(TestTriads PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/../src
    ${CMAKE_CURRENT_SOURCE_DIR}/../vendor/catch2
)

# Link the Catch2 library
target_link_libraries(TestTriads PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/../build/libTriadsLib.a
)