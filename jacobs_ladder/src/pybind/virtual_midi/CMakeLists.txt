cmake_minimum_required(VERSION 3.14)

# Set the project name
project(teVirtualMIDITest VERSION 1.0)

# Use C++17 standard for Pybind11
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set C99 standard for C files
set(CMAKE_C_STANDARD 99)

# Define _CRT_SECURE_NO_WARNINGS to suppress deprecation warnings
add_definitions(-D_CRT_SECURE_NO_WARNINGS)

# Include current directory for header files
include_directories("${CMAKE_SOURCE_DIR}")

# Detect architecture (64-bit or 32-bit) and link the correct library
if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    message(STATUS "64-bit architecture detected, linking teVirtualMIDI64.lib")
    set(TEVIRTUALMIDI_LIB "${CMAKE_SOURCE_DIR}/teVirtualMIDI64.lib")
elseif(CMAKE_SIZEOF_VOID_P EQUAL 4)
    message(STATUS "32-bit architecture detected, linking teVirtualMIDI32.lib")
    set(TEVIRTUALMIDI_LIB "${CMAKE_SOURCE_DIR}/teVirtualMIDI32.lib")
else()
    message(FATAL_ERROR "Unknown architecture")
endif()

# -------------------------------
# ADD nlohmann/json
# -------------------------------
include(FetchContent)
FetchContent_Declare(
    nlohmann_json
    GIT_REPOSITORY https://github.com/nlohmann/json.git
    GIT_TAG v3.10.4  # Specify the desired version (latest stable at time of writing)
)
FetchContent_MakeAvailable(nlohmann_json)

# -------------------------------
# BUILD EXECUTABLES
# -------------------------------
# Build the original executable
add_executable(teVirtualMIDITest teVirtualMIDITest.c)
target_link_libraries(teVirtualMIDITest PRIVATE "${TEVIRTUALMIDI_LIB}" nlohmann_json::nlohmann_json)

# Set runtime output directory for the executable
set_target_properties(teVirtualMIDITest PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

# Build the second executable from VirtualMidi.cpp
add_executable(VirtualMidi2Executable VirtualMidi2.cpp)
target_link_libraries(VirtualMidi2Executable PRIVATE "${TEVIRTUALMIDI_LIB}" nlohmann_json::nlohmann_json)

# Set runtime output directory for the new executable
set_target_properties(VirtualMidi2Executable PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

# Debug output
message(STATUS "CMAKE_SOURCE_DIR: ${CMAKE_SOURCE_DIR}")
