cmake_minimum_required(VERSION 3.0)

#---------------------------------------------------------------------------------------
# Start livox_ros_driver2 project
#---------------------------------------------------------------------------------------
include(cmake/version.cmake)
project(livox_ros_driver2 VERSION ${LIVOX_ROS_DRIVER2_VERSION} LANGUAGES CXX)
message(STATUS "livox_ros_driver2 version: ${LIVOX_ROS_DRIVER2_VERSION}")

#---------------------------------------------------------------------------------------
# Add ROS Version MACRO
#---------------------------------------------------------------------------------------
if(DEFINED ENV{ROS_VERSION} AND $ENV{ROS_VERSION} EQUAL 1)
    add_definitions(-DBUILDING_ROS1)
    message(STATUS "Building for ROS1")
else()
    message(FATAL_ERROR "Unsupported ROS version or ROS_VERSION environment variable not set.")
endif()

#---------------------------------------------------------------------------------------
# Find package and the dependency
#---------------------------------------------------------------------------------------
find_package(Boost 1.54 REQUIRED COMPONENTS
  system
  thread
  chrono
)

# Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  sensor_msgs
  std_msgs
  message_generation
  rosbag
  pcl_ros
)

# Find pcl lib
find_package(PCL REQUIRED)

# Generate messages in the 'msg' folder
add_message_files(FILES
  CustomPoint.msg
  CustomMsg.msg
)

# Generate added messages and services with any dependencies listed here
generate_messages(DEPENDENCIES
  std_msgs
)

find_package(PkgConfig)
pkg_check_modules(APR apr-1)
if (APR_FOUND)
  message(${APR_INCLUDE_DIRS})
  message(${APR_LIBRARIES})
endif (APR_FOUND)

# Catkin specific configuration
catkin_package(CATKIN_DEPENDS
  roscpp rospy std_msgs message_runtime pcl_ros
)

# Set default build to release
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose Release or Debug" FORCE)
endif()

# Compiler config
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Make sure the livox_lidar_sdk_static library is installed
find_library(LIVOX_LIDAR_SDK_LIBRARY liblivox_lidar_sdk_static.a /usr/local/lib)

# PCL library
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

# Generate executable and add libraries
add_executable(${PROJECT_NAME}_node
  src/driver_node.cpp
  src/lds.cpp
  src/lds_lidar.cpp
  src/lddc.cpp
  src/livox_ros_driver2.cpp

  src/comm/comm.cpp
  src/comm/ldq.cpp
  src/comm/semaphore.cpp
  src/comm/lidar_imu_data_queue.cpp
  src/comm/cache_index.cpp
  src/comm/pub_handler.cpp

  src/parse_cfg_file/parse_cfg_file.cpp
  src/parse_cfg_file/parse_livox_lidar_cfg.cpp

  src/call_back/lidar_common_callback.cpp
  src/call_back/livox_lidar_callback.cpp
)

# Precompile macro and compile option
target_compile_options(${PROJECT_NAME}_node
  PRIVATE $<$<CXX_COMPILER_ID:GNU>:-Wall>
)

# Add projects that depend on
add_dependencies(${PROJECT_NAME}_node ${PROJECT_NAME}_generate_messages_cpp)

# Source file
target_sources(${PROJECT_NAME}_node
  PRIVATE
  src/driver_node.cpp
  src/lds.cpp
  src/lds_lidar.cpp
  src/lddc.cpp
  src/livox_ros_driver2.cpp

  src/comm/comm.cpp
  src/comm/ldq.cpp
  src/comm/semaphore.cpp
  src/comm/lidar_imu_data_queue.cpp
  src/comm/cache_index.cpp
  src/comm/pub_handler.cpp

  src/parse_cfg_file/parse_cfg_file.cpp
  src/parse_cfg_file/parse_livox_lidar_cfg.cpp

  src/call_back/lidar_common_callback.cpp
  src/call_back/livox_lidar_callback.cpp
)

# Include file
target_include_directories(${PROJECT_NAME}_node
  PUBLIC
  ${catkin_INCLUDE_DIRS}
  ${PCL_INCLUDE_DIRS}
  ${APR_INCLUDE_DIRS}
  3rdparty
  src
)

# Link libraries
target_link_libraries(${PROJECT_NAME}_node
  ${LIVOX_LIDAR_SDK_LIBRARY}
  ${Boost_LIBRARIES}
  ${catkin_LIBRARIES}
  ${PCL_LIBRARIES}
  ${APR_LIBRARIES}
)

# Install
install(TARGETS ${PROJECT_NAME}_node
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch_ROS1/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch_ROS1
)
