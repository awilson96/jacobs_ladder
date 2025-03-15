cmake_minimum_required(VERSION 3.14)

# Use C++17 standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set C99 standard for C files
set(CMAKE_C_STANDARD 99)

# Define _CRT_SECURE_NO_WARNINGS to suppress deprecation warnings
add_definitions(-D_CRT_SECURE_NO_WARNINGS)

# Include directories for headers
include_directories("${CMAKE_SOURCE_DIR}/cpp/include")
include_directories("${CMAKE_SOURCE_DIR}/cpp/external")

# Detect architecture (64-bit or 32-bit) and link the correct library
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
