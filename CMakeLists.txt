cmake_minimum_required(VERSION 2.2.2)
project(NAFF)

add_compile_options(-std=c++11 -O3 -Wall -Wextra -pedantic)
file(GLOB HEADER_FILES "*.h")
file(GLOB SOURCE_FILES "*.cc")


#--------Python-----------#find_package(PythonLibs 2.7  REQUIRED)

find_package(PythonLibs 2.7 EXACT REQUIRED)
message("Include dir for Python: " ${PYTHON_INCLUDE_DIR} )
message("Libs of Python: " ${PYTHON_LIBRARIES} )


#--------BOOST-----------#

find_package(Boost COMPONENTS python REQUIRED)
message("Include dirs of boost: " ${Boost_INCLUDE_DIRS} )
message("Libs of boost: " ${Boost_LIBRARIES} )


#--------Linking FFTW-----------#

find_path(FFTW3_INCLUDE_DIR fftw3.h fftw.h)
find_library(FFTW3_LIBRARIES NAMES fftw3 libfftiw3 fftw)
if(NOT FFTW3_INCLUDE_DIR OR NOT FFTW3_LIBRARIES)
  message(FATAL_ERROR "Could not find fftw3.")
else ()
  message("-- Linking FFTW...")
endif()

include_directories(
	${FFTW3_INCLUDES}
	${Boost_INCLUDE_DIRS}
	${PYTHON_INCLUDE_DIRS}
)
LINK_LIBRARIES(${Boost_LIBRARIES} ${PYTHON_LIBRARIES} ${FFTW3_LIBRARIES})

## Uncomment to create NAFF.so and import to python
add_library(NAFF SHARED interface_NAFF.cpp ${SOURCE_FILES} ${HEADER_FILES})


#add_executable (NAFF main_NAFF.cpp ${SOURCE_FILES} ${HEADER_FILES})
target_link_libraries(NAFF 
	${Boost_LIBRARIES} 
	${PYTHON_LIBRARIES} 
	${FFTW3_LIBRARIES}
)
set_target_properties(NAFF PROPERTIES PREFIX ""
	LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

