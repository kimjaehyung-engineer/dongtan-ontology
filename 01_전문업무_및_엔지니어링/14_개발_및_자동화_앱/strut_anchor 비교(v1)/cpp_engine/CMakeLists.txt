cmake_minimum_required(VERSION 3.15)
project(EarthRetainingFEMEngine CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

add_executable(earth_retaining_cli src/main_cli.cpp)

# Windows MSVC / MinGW 컴파일 옵션
if(MSVC)
    target_compile_options(earth_retaining_cli PRIVATE /W4 /O2 /utf-8)
else()
    target_compile_options(earth_retaining_cli PRIVATE -Wall -Wextra -O3)
endif()
