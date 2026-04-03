cmake_minimum_required(VERSION 3.20)
project(HypercubeHopfieldPython LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(pybind11 CONFIG REQUIRED)

# Architecture selection for cross-platform wheels
set(HYPERCUBE_ARCH "native" CACHE STRING "Target arch: native | x86-64-v2 | none")

set(CORE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/..")
set(CORE_SOURCES "${CORE_DIR}/HopfieldNetwork.cpp")

pybind11_add_module(_core bindings.cpp ${CORE_SOURCES})

target_include_directories(_core PRIVATE ${CORE_DIR})

# Optimization flags
if(MSVC)
    target_compile_options(_core PRIVATE /O2 /fp:fast)
else()
    target_compile_options(_core PRIVATE -O3 -ffast-math)
    if(HYPERCUBE_ARCH STREQUAL "native")
        target_compile_options(_core PRIVATE -march=native -mtune=native)
    elseif(HYPERCUBE_ARCH STREQUAL "x86-64-v2")
        target_compile_options(_core PRIVATE -march=x86-64-v2 -mtune=generic)
    endif()
    # "none" = no -march flag (ARM, MSVC fallback)
endif()

# MinGW: static-link runtime DLLs for self-contained .pyd
if(MINGW)
    target_link_options(_core PRIVATE
        -static-libgcc -static-libstdc++
        -static
    )
endif()

install(TARGETS _core DESTINATION hypercube_hopfield)
