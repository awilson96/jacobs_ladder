cmake_minimum_required(VERSION 3.14)
project(MyProject)

# Use C++17 standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Define _CRT_SECURE_NO_WARNINGS to suppress deprecation warnings
add_definitions(-D_CRT_SECURE_NO_WARNINGS)

# Include directories
include_directories("${CMAKE_SOURCE_DIR}/cpp/include")
include_directories("${CMAKE_SOURCE_DIR}/cpp/external")
include_directories("${CMAKE_SOURCE_DIR}/src")

# Detect architecture and set the appropriate library
if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    message(STATUS "64-bit architecture detected, linking teVirtualMIDI64.lib")
    set(TEVIRTUALMIDI_LIB "${CMAKE_SOURCE_DIR}/cpp/lib/teVirtualMIDI64.lib")
elseif(CMAKE_SIZEOF_VOID_P EQUAL 4)
    message(STATUS "32-bit architecture detected, linking teVirtualMIDI32.lib")
    set(TEVIRTUALMIDI_LIB "${CMAKE_SOURCE_DIR}/cpp/lib/teVirtualMIDI32.lib")
else()
    message(FATAL_ERROR "Unknown architecture")
endif()

# -------------------------------
# PYBIND11 CONFIGURATION
# -------------------------------
find_package(pybind11 REQUIRED)

# Get all source and header files
file(GLOB_RECURSE SOURCES src/*.cpp)
file(GLOB_RECURSE HEADERS src/*.h)

# Separate test files and normal sources
set(TEST_SOURCES "")
set(NORMAL_SOURCES "")

foreach(FILE ${SOURCES})
    if(FILE MATCHES ".*Test\\.cpp$")
        list(APPEND TEST_SOURCES ${FILE})
    else()
        list(APPEND NORMAL_SOURCES ${FILE})
    endif()
endforeach()

# Add a shared library for the Python module
add_library(virtual_midi MODULE ${NORMAL_SOURCES})
target_include_directories(virtual_midi PRIVATE "${CMAKE_SOURCE_DIR}/src")
target_link_libraries(virtual_midi PRIVATE pybind11::module "${TEVIRTUALMIDI_LIB}")

# Ensure correct naming for Python module
set_target_properties(virtual_midi PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
    PREFIX ""  
    SUFFIX ".pyd"
)

# -------------------------------
# BUILD EXECUTABLES
# -------------------------------
add_executable(teVirtualMIDITest src/teVirtualMIDITest.c)
target_link_libraries(teVirtualMIDITest PRIVATE "${TEVIRTUALMIDI_LIB}")
set_target_properties(teVirtualMIDITest PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

add_executable(VirtualMidiPortScript src/VirtualMidiPortScript.cpp)
target_link_libraries(VirtualMidiPortScript PRIVATE "${TEVIRTUALMIDI_LIB}")
set_target_properties(VirtualMidiPortScript PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

# -------------------------------
# AUTO-DETECTED TESTS
# -------------------------------
foreach(TEST_FILE ${TEST_SOURCES})
    get_filename_component(TEST_NAME ${TEST_FILE} NAME_WE)
    add_executable(${TEST_NAME} ${TEST_FILE})
    target_link_libraries(${TEST_NAME} PRIVATE virtual_midi "${TEVIRTUALMIDI_LIB}")
    set_target_properties(${TEST_NAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
    add_test(NAME ${TEST_NAME} COMMAND ${TEST_NAME})
endforeach()

# Enable testing
enable_testing()

# Debug output
message(STATUS "CMAKE_SOURCE_DIR: ${CMAKE_SOURCE_DIR}")
