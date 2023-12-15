cmake_minimum_required(VERSION 3.13)
project(test_cmake CXX)
cmake_policy(VERSION 3.27)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_STANDARD 20)


#### test ####
add_executable(test1 ./tests/test1.cpp)

