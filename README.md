# UMIC_Project_Team1
## THE TRACKING &amp; NAVIGATION CHALLENGE

### PREREQUISITE PACKAGES NEEDED
1. PyTorch for ML implementation
2. OpenCV for countour detection
3. ROS and Gazebo for simulation

## PROCEDURE

### Setting up the Workspace

1. Install the above packages before eveything else
2. Copy the folder 'frames' in .gazebo/models
3. Build the workspace mybot_ws(Project)

### INDIVIDUAL ASPECT TESTING

#### Frontier+CV

1. ./run_world.sh
2. ./run_add.sh
3. roslaunch mybot_navigation move_base.launch
4. python image_converter.py
5. roslaunch mybot_gazebo mybot_trigger1.launch

#### Wall Follower

1. ./run_world.sh
2. ./run_add.sh
3. Move the robot and orient it towards the passage in Gazebo
4. ./run_wf.sh 

## FINAL TESTING (ALL IN ONE)

1. ./run_gazebo.sh
2.  roslaunch mybot_gazebo mybot_trigger1.launch
3.  python image_converter.py
4.  roslaunch mybot_navigation move_base.launch
