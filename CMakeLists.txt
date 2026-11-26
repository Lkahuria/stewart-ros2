cmake_minimum_required(VERSION 3.16)
project(stewart)

find_package(ament_cmake REQUIRED)

install(PROGRAMS
  scripts/ik.py
  scripts/ps4_controller.py
  scripts/wave_demo.py
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch sdf world
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
