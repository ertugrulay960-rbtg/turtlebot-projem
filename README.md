# TurtleBot3 Waypoint Navigation Odevi

## Gereksinimler
- Ubuntu 20.04
- ROS Noetic
- TurtleBot3 paketleri

## TurtleBot3 Kurulumu

```bash
sudo apt install ros-noetic-joy ros-noetic-teleop-twist-joy ros-noetic-teleop-twist-keyboard ros-noetic-laser-proc ros-noetic-rgbd-launch ros-noetic-rosserial-arduino ros-noetic-rosserial-python ros-noetic-rosserial-client ros-noetic-rosserial-msgs ros-noetic-amcl ros-noetic-map-server ros-noetic-move-base ros-noetic-urdf ros-noetic-xacro ros-noetic-compressed-image-transport ros-noetic-rviz ros-noetic-gmapping ros-noetic-navigation ros-noetic-interactive-markers -y
```

```bash
cd ~/catkin_ws/src
git clone -b noetic https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
git clone -b noetic https://github.com/ROBOTIS-GIT/turtlebot3.git
git clone -b noetic https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
cd ~/catkin_ws && catkin_make
source ~/catkin_ws/devel/setup.bash
```

## Calistirma

Terminal 1 - Gazebo:
```bash
export TURTLEBOT3_MODEL=waffle
roslaunch turtlebot3_gazebo turtlebot3_world.launch
```

Terminal 2 - Navigation:
```bash
export TURTLEBOT3_MODEL=waffle
roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$(pwd)/harita.yaml
```

Terminal 3 - RViz'de 2D Pose Estimate ile robotu haritada dogru konuma getir, sonra:
```bash
python3 waypoint_nav.py
```

## Sonuc
Robot sirasiyla 5 farkli noktaya otonom olarak gider.
