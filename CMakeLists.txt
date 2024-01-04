cmake_minimum_required(VERSION 3.13)
project(test_cmake CXX)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-arcs -ftest-coverage")
set(CMAKE_CXX_OUTPUT_EXTENSION_REPLACE 1)


#### test ####
add_executable(test1 ./tests/test1.cpp)
add_executable(test2 ./tests/test2.cpp)
add_executable(test3 ./tests/test3.cpp)

