cmake_minimum_required(VERSION 3.26)
project(ClangScraper)

# Set C++ standard
set(CMAKE_CXX_STANDARD 20)
#set(CMAKE_CXX_COMPILER "/c/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/Llvm/bin/clang++")
set(CMAKE_CXX_COMPILER "clang++")

# Add source files
add_executable(ClangScraper main.cpp)

# add_subdirectory(components)

# Optional: Include additional directories
# include_directories(include)

# Optional: Link against libraries
# target_link_libraries(MyExecutable mylib)

# Optional: Set compiler options
# target_compile_options(MyExecutable PRIVATE -Wall -Wextra)
