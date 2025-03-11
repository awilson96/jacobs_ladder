cmake_minimum_required(VERSION 3.10)

# Set the project name and version
project(teVirtualMIDITest VERSION 1.0)

# Specify the C standard to use
set(CMAKE_C_STANDARD 99)

# Define _CRT_SECURE_NO_WARNINGS to suppress deprecation warnings
add_definitions(-D_CRT_SECURE_NO_WARNINGS)

# Add executable
add_executable(teVirtualMIDITest teVirtualMIDITest.c)

# Include the current directory for the header files
include_directories("${CMAKE_SOURCE_DIR}")

# Conditionally link the correct library based on architecture
if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    # 64-bit architecture
    message(STATUS "64-bit architecture detected, linking teVirtualMIDI64.lib")
    target_link_libraries(teVirtualMIDITest "${CMAKE_SOURCE_DIR}/teVirtualMIDI64.lib")
elseif(CMAKE_SIZEOF_VOID_P EQUAL 4)
    # 32-bit architecture
    message(STATUS "32-bit architecture detected, linking teVirtualMIDI32.lib")
    target_link_libraries(teVirtualMIDITest "${CMAKE_SOURCE_DIR}/teVirtualMIDI32.lib")
else()
    message(FATAL_ERROR "Unknown architecture")
endif()

# Set runtime output directory
set_target_properties(teVirtualMIDITest PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

# Debug output
message(STATUS "CMAKE_SOURCE_DIR: ${CMAKE_SOURCE_DIR}")
