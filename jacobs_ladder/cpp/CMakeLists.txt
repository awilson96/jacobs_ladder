cmake_minimum_required(VERSION 3.16)
project(JacobsLadder CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Optimization flags (Release only)
set(CMAKE_CXX_FLAGS_RELEASE
    "${CMAKE_CXX_FLAGS_RELEASE} -O3 -flto -march=native -funroll-loops"
)

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------

set(BIN_DIR ${CMAKE_SOURCE_DIR}/bin)

# ------------------------------------------------------------------
# Clean bin directory
# ------------------------------------------------------------------

add_custom_target(clean_bin
    COMMAND ${CMAKE_COMMAND} -E remove_directory ${BIN_DIR}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${BIN_DIR}
    COMMENT "Cleaning and recreating ${BIN_DIR}"
)

# ------------------------------------------------------------------
# Source discovery
# ------------------------------------------------------------------

file(GLOB_RECURSE SRC_FILES CONFIGURE_DEPENDS
    src/*.cpp
    src/*.h
)

file(GLOB_RECURSE EXT_FILES CONFIGURE_DEPENDS
    external/*.cpp
    external/*.h
    external/*.hpp
)

# EXCLUDE RtMidi sources (built separately)
list(FILTER EXT_FILES EXCLUDE REGEX ".*/external/rtmidi/.*")

file(GLOB_RECURSE TEST_FILES CONFIGURE_DEPENDS
    test/*.cpp
)

file(GLOB_RECURSE PYBIND_FILES CONFIGURE_DEPENDS
    pybind/*.cpp
)

# ------------------------------------------------------------------
# Pybind11
# ------------------------------------------------------------------

find_package(pybind11 REQUIRED)

# ------------------------------------------------------------------
# Platform system libraries
# ------------------------------------------------------------------

set(PLATFORM_LIBS "")

if(WIN32)
    list(APPEND PLATFORM_LIBS winmm)
elseif(APPLE)
    find_library(COREMIDI_LIBRARY CoreMIDI REQUIRED)
    find_library(COREFOUNDATION_LIBRARY CoreFoundation REQUIRED)
    list(APPEND PLATFORM_LIBS
        ${COREMIDI_LIBRARY}
        ${COREFOUNDATION_LIBRARY}
    )
elseif(UNIX)
    list(APPEND PLATFORM_LIBS pthread asound)
endif()

# ------------------------------------------------------------------
# Windows-only vendor MIDI libraries (teVirtualMIDI, etc.)
# ------------------------------------------------------------------

set(WINDOWS_VENDOR_LIBS "")

if(WIN32)
    file(GLOB WINDOWS_VENDOR_LIBS
        ${CMAKE_SOURCE_DIR}/lib/teVirtualMIDI*.lib
        ${CMAKE_SOURCE_DIR}/external/lib/teVirtualMIDI*.lib
    )

    if(WINDOWS_VENDOR_LIBS)
        message(STATUS "Using Windows vendor MIDI libs: ${WINDOWS_VENDOR_LIBS}")
    endif()
endif()

# ------------------------------------------------------------------
# Include paths
# ------------------------------------------------------------------

include_directories(
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_SOURCE_DIR}/external
    ${CMAKE_SOURCE_DIR}/external/catch2
    ${CMAKE_SOURCE_DIR}/external/rtmidi
)

# ------------------------------------------------------------------
# RtMidi shared library (single source of truth)
# ------------------------------------------------------------------

add_library(RtMidiLib SHARED
    external/rtmidi/RtMidi.cpp
    external/rtmidi/rtmidi_c.cpp
)

target_include_directories(RtMidiLib
    PUBLIC ${CMAKE_SOURCE_DIR}/external/rtmidi
)

# Define platform-specific compile flags for RtMidi
if(APPLE)
    target_compile_definitions(RtMidiLib PRIVATE __MACOSX_CORE__)
    target_link_libraries(RtMidiLib
        PUBLIC
            "-framework CoreMIDI"
            "-framework CoreFoundation"
            "-framework CoreAudio"
    )
elseif(UNIX)
    target_compile_definitions(RtMidiLib PRIVATE __LINUX_ALSA__)
    target_link_libraries(RtMidiLib PUBLIC asound pthread)
elseif(WIN32)
    target_compile_definitions(RtMidiLib PRIVATE _WINDOWS)
endif()

set_target_properties(RtMidiLib PROPERTIES
    OUTPUT_NAME rtmidi
)

# ------------------------------------------------------------------
# Main static library
# ------------------------------------------------------------------

add_library(MyLib STATIC
    ${SRC_FILES}
    ${EXT_FILES}
)

target_link_libraries(MyLib
    PRIVATE
        RtMidiLib
        ${PLATFORM_LIBS}
        ${WINDOWS_VENDOR_LIBS}
)

# ------------------------------------------------------------------
# Test executables
# ------------------------------------------------------------------

foreach(test_file ${TEST_FILES})
    get_filename_component(test_name ${test_file} NAME_WE)

    add_executable(${test_name} ${test_file})

    target_link_libraries(${test_name}
        PRIVATE
            MyLib
            ${WINDOWS_VENDOR_LIBS}
    )

    if("${test_file}" MATCHES ".*Test\\.cpp$")
        target_link_libraries(${test_name} PRIVATE ${PLATFORM_LIBS})
    endif()
endforeach()

# ------------------------------------------------------------------
# Pybind modules
# ------------------------------------------------------------------

foreach(pybind_file ${PYBIND_FILES})
    get_filename_component(module_name ${pybind_file} NAME_WE)

    message(STATUS "Generating Pybind module: ${module_name}")

    pybind11_add_module(${module_name} ${pybind_file})

    target_link_libraries(${module_name}
        PRIVATE
            MyLib
            RtMidiLib
            ${WINDOWS_VENDOR_LIBS}
    )

    set_target_properties(${module_name} PROPERTIES
        OUTPUT_NAME ${module_name}
    )
endforeach()

# ------------------------------------------------------------------
# Output handling
# ------------------------------------------------------------------

file(MAKE_DIRECTORY ${BIN_DIR})

foreach(test_file ${TEST_FILES})
    get_filename_component(test_name ${test_file} NAME_WE)

    add_custom_command(TARGET ${test_name} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
            $<TARGET_FILE:${test_name}>
            ${BIN_DIR}/$<TARGET_FILE_NAME:${test_name}>
    )
endforeach()

set(PYBIND_TARGET_DIR ${CMAKE_SOURCE_DIR}/../)
file(MAKE_DIRECTORY ${PYBIND_TARGET_DIR})

foreach(pybind_file ${PYBIND_FILES})
    get_filename_component(module_name ${pybind_file} NAME_WE)

    add_custom_command(TARGET ${module_name} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
            $<TARGET_FILE:${module_name}>
            ${PYBIND_TARGET_DIR}/$<TARGET_FILE_NAME:${module_name}>
        COMMAND ${CMAKE_COMMAND} -E rename
            ${PYBIND_TARGET_DIR}/$<TARGET_FILE_NAME:${module_name}>
            ${PYBIND_TARGET_DIR}/${module_name}.pyd
    )
endforeach()
