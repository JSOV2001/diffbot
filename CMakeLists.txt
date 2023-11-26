cmake_minimum_required(VERSION 3.8)
project(diffbot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Dependencias de ROS2
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

# Python
ament_python_install_package(scripts)
install(PROGRAMS
  scripts/joint_group_velocity_publisher.py
  scripts/teleop_twist_publisher.py
  DESTINATION lib/${PROJECT_NAME}
)

# Carpetas Adicionales
install(
  DIRECTORY config description launch
  DESTINATION share/${PROJECT_NAME}
)


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
