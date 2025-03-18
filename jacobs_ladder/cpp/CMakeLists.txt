cmake_minimum_required(VERSION 3.14)

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
find_package(pybind11 REQUIRED)  # Ensure pybind11 is installed

# Add a shared library for the Python module
add_library(virtual_midi MODULE src/VirtualMidiManager.cpp)

# Include the header file for the source file
target_include_directories(virtual_midi PRIVATE "${CMAKE_SOURCE_DIR}/src")  # Ensure the header is included

# Link necessary libraries
target_link_libraries(virtual_midi PRIVATE pybind11::module "${TEVIRTUALMIDI_LIB}")

# Ensure the output file has the correct naming convention for Python modules
set_target_properties(virtual_midi PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
    PREFIX ""  # Remove "lib" prefix (important for Windows)
    SUFFIX ".pyd"  # Use `.pyd` on Windows
)

# -------------------------------
# BUILD EXECUTABLES
# -------------------------------
add_executable(teVirtualMIDITest src/teVirtualMIDITest.c)
target_link_libraries(teVirtualMIDITest PRIVATE "${TEVIRTUALMIDI_LIB}")

add_executable(VirtualMidi2Executable src/VirtualMidi2.cpp)
target_link_libraries(VirtualMidi2Executable PRIVATE "${TEVIRTUALMIDI_LIB}")

# Set runtime output directory for executables
set_target_properties(teVirtualMIDITest PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
set_target_properties(VirtualMidi2Executable PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

# Debug output
message(STATUS "CMAKE_SOURCE_DIR: ${CMAKE_SOURCE_DIR}")
