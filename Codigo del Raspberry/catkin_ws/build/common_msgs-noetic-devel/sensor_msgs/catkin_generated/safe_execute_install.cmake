execute_process(COMMAND "/home/pi/catkin_ws/build/common_msgs-noetic-devel/sensor_msgs/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/pi/catkin_ws/build/common_msgs-noetic-devel/sensor_msgs/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
