cmake_minimum_required(VERSION 3.16)
project(JacobsLadder CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set optimization flags for maximal optimization (O3, LTO, and other flags)
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3 -flto -march=native -funroll-loops")

# Define the bin directory relative to the project root
set(BIN_DIR ${CMAKE_SOURCE_DIR}/bin)

# Remove the bin directory before recompilation
add_custom_target(clean_bin
    COMMAND ${CMAKE_COMMAND} -E remove_directory ${BIN_DIR}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${BIN_DIR}
    COMMENT "Cleaning and recreating ${BIN_DIR}"
)

# Detect all .cpp and .h files in src/
file(GLOB_RECURSE SRC_FILES CONFIGURE_DEPENDS src/*.cpp src/*.h)

# Detect all .cpp, .h, and .hpp files in external/
file(GLOB_RECURSE EXT_FILES CONFIGURE_DEPENDS external/*.cpp external/*.h external/*.hpp)

# Detect all .cpp files in test/ (each will be a separate executable)
file(GLOB_RECURSE TEST_FILES CONFIGURE_DEPENDS test/*.cpp)

# Pybind11 Integration - Use a dedicated /pybind directory
file(GLOB_RECURSE PYBIND_FILES CONFIGURE_DEPENDS pybind/*.cpp)

# Find Pybind11
find_package(pybind11 REQUIRED)

# Set default libraries based on platform
set(DEFAULT_LIBS pybind11::module)  # Always include pybind11

if(WIN32)
    list(APPEND DEFAULT_LIBS winmm)  # Windows Multimedia Library for QueryPerformanceCounter
elseif(UNIX)
    list(APPEND DEFAULT_LIBS pthread)  # Pthreads for POSIX systems
endif()

# Search for all libraries in /lib and /external/lib
file(GLOB ALL_LIB_FILES CONFIGURE_DEPENDS lib/* external/lib/*)

# Start empty
set(LIB_FILES_TO_LINK)

# Filter libraries based on platform
foreach(libfile ${ALL_LIB_FILES})
    get_filename_component(libname ${libfile} NAME)  # just the filename
    if(WIN32)
        # On Windows, include everything
        list(APPEND LIB_FILES_TO_LINK ${libfile})
    elseif(UNIX)
        # On macOS/Linux, skip Windows-only .lib files
        if(NOT libname MATCHES ".*\\.lib$")
            list(APPEND LIB_FILES_TO_LINK ${libfile})
        else()
            message(STATUS "Skipping Windows-only library on macOS/Linux: ${libname}")
        endif()
    endif()
endforeach()

if(LIB_FILES_TO_LINK)
    message(STATUS "Libraries to link: ${LIB_FILES_TO_LINK}")
endif()

# Add external/ and src/ directories to include paths for all targets
include_directories(${CMAKE_SOURCE_DIR}/src ${CMAKE_SOURCE_DIR}/external ${CMAKE_SOURCE_DIR}/external/catch2)

# Create a static library from src/ and external/
add_library(MyLib STATIC ${SRC_FILES} ${EXT_FILES})

# Link filtered libraries + default libraries
target_link_libraries(MyLib PRIVATE ${LIB_FILES_TO_LINK} ${DEFAULT_LIBS})

# Add the src/ directory to include paths for all targets
include_directories(${CMAKE_SOURCE_DIR}/src)

# Process each test file separately as an executable
foreach(test_file ${TEST_FILES})
    get_filename_component(test_name ${test_file} NAME_WE)
    add_executable(${test_name} ${test_file})
    target_link_libraries(${test_name} PRIVATE MyLib)
    # Only link Catch2 if the filename ends with Test.cpp
    if("${test_file}" MATCHES ".*Test\\.cpp$")
        target_link_libraries(${test_name} PRIVATE ${DEFAULT_LIBS})
    endif()
endforeach()

# Pybind11 Integration - Automatically detect files meant for Pybind modules
foreach(pybind_file ${PYBIND_FILES})
    get_filename_component(module_name ${pybind_file} NAME_WE)
    message(STATUS "Generating Pybind module: ${module_name}")
    pybind11_add_module(${module_name} ${pybind_file})
    set_target_properties(${module_name} PROPERTIES OUTPUT_NAME ${module_name})
    target_link_libraries(${module_name} PRIVATE MyLib ${DEFAULT_LIBS})
endforeach()

# Define the bin directory relative to the project root
set(BIN_DIR ${CMAKE_SOURCE_DIR}/bin)

# Ensure the bin directory exists
file(MAKE_DIRECTORY ${BIN_DIR})

# Copy all test executables to /bin
foreach(test_file ${TEST_FILES})
    get_filename_component(test_name ${test_file} NAME_WE)
    add_custom_command(TARGET ${test_name} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${test_name}> ${BIN_DIR}/$<TARGET_FILE_NAME:${test_name}>
        COMMENT "Copying ${test_name} to ${BIN_DIR}"
    )
endforeach()

# Define the target directory as ../ (parent directory of the project)
set(PYBIND_TARGET_DIR ${CMAKE_SOURCE_DIR}/../)

# Ensure the target directory exists
file(MAKE_DIRECTORY ${PYBIND_TARGET_DIR})

# Copy all Pybind11 modules to /bin (if applicable)
foreach(pybind_file ${PYBIND_FILES})
    get_filename_component(module_name ${pybind_file} NAME_WE)
    message(STATUS "Generating Pybind module2: ${module_name}")
    add_custom_command(TARGET ${module_name} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${module_name}> ${PYBIND_TARGET_DIR}/$<TARGET_FILE_NAME:${module_name}>
        COMMAND ${CMAKE_COMMAND} -E rename ${PYBIND_TARGET_DIR}/$<TARGET_FILE_NAME:${module_name}> ${PYBIND_TARGET_DIR}/${module_name}.pyd
        COMMENT "Copying and renaming ${module_name} to ${PYBIND_TARGET_DIR}/${module_name}.pyd"
    )
endforeach()
