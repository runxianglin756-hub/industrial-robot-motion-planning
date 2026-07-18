Stage 1: Basic Knowledge of Six-Axis Industrial Robots

1. What is a Six-Axis Industrial Robot?

A six-axis industrial robot is a robot arm with six rotating joints.

It can move its end tool to different positions and directions in 3D space.

In simple words:

Six-axis robot = a robot arm with 6 rotating joints

It is commonly used for:

- Pick and place
- Assembly
- Welding
- Loading and unloading
- Material handling


2. What Do the Six Joints Do?

Each joint controls one part of the robot arm.

Joint 1: Rotates the robot base
Joint 2: Moves the shoulder
Joint 3: Moves the elbow
Joint 4: Rotates the wrist
Joint 5: Bends the wrist
Joint 6: Rotates the end tool

My understanding is that one joint cannot finish the whole motion alone. All joints work together to move the robot arm.


3. What is an End-Effector?

The end-effector is the tool at the end of the robot arm.

Examples:

- Gripper
- Suction cup
- Welding tool
- Screwdriver
- Camera

In a pick-and-place task, the end-effector is usually used to grab and place objects.

In simple words:

End-effector = the tool on the robot hand


4. Position and Orientation

A robot end-effector needs both position and orientation.

Position means where the tool is:

x, y, z

Orientation means which direction the tool is facing.

In simple words:

Position = where it is
Orientation = where it faces


5. What is a Coordinate System?

A coordinate system is used to describe position and direction.

Robots usually have many coordinate systems:

- World coordinate system
- Robot base coordinate system
- Joint coordinate systems
- End-effector coordinate system

In simple words:

Coordinate system = a reference used to describe position and direction


6. What is Forward Kinematics?

Forward kinematics means:

Given joint angles -> find the end-effector position

For example, if we know all joint angles, we can calculate where the robot hand is.

In simple words:

Forward kinematics = joint angles to robot hand position


7. What is Inverse Kinematics?

Inverse kinematics means:

Given a target position -> find the required joint angles

For example, if we want the robot hand to reach a point, inverse kinematics tells each joint how to move.

In simple words:

Inverse kinematics = target position to joint angles

Inverse kinematics is harder because one target may have more than one possible solution.


8. What are DH Parameters?

DH parameters are used to describe the structure of a robot arm.

They describe the relationship between links and joints.

There are four main DH parameters:

theta: Joint angle
d: Offset distance
a: Link length
alpha: Twist angle

In simple words:

DH parameters = a table that describes the robot arm structure


9. What is a Homogeneous Transformation Matrix?

A homogeneous transformation matrix is a 4 by 4 matrix.

It can describe:

- Rotation
- Movement
- Coordinate transformation

In robotics, each joint has a transformation matrix. Multiplying all matrices gives the final position and orientation of the end-effector.

In simple words:

Transformation matrix = a tool to calculate how the robot arm moves from one joint to the next


10. What is URDF?

URDF is a file format used to describe robot models.

It can describe:

- Links
- Joints
- Joint limits
- Shape
- Mass
- Collision model

In simple words:

URDF = the digital instruction file of a robot

PyBullet can load a URDF file and show the robot in simulation.


11. What is PyBullet?

PyBullet is a robot simulation tool.

It can:

- Open a 3D simulation window
- Load robot models
- Simulate gravity
- Control robot joints
- Test robot motion
- Detect collisions

In simple words:

PyBullet = software that simulates robot motion on a computer


12. What I Have Completed

So far, I have completed:

- Installed Python and Conda environment
- Installed PyBullet
- Opened the PyBullet GUI
- Loaded a ground plane
- Loaded a robot arm model
- Printed joint information
- Controlled the robot joints
- Made the robot arm move in simulation

Currently, I used the built-in KUKA robot model for testing. Next, I will try to import the UR5 robot model.


13. Stage 1 Summary

In Stage 1, I learned the basic concepts of six-axis industrial robots.

A six-axis robot is a robot arm with six rotating joints. By controlling these joints, the robot can move its end-effector to different positions and directions.

Forward kinematics calculates the end-effector position from joint angles. Inverse kinematics calculates joint angles from a target position.

DH parameters and transformation matrices are important tools for describing robot structure and motion.

URDF is used to describe robot models, and PyBullet is used to simulate robot motion.

The next step is to load the UR5 model and continue learning robot kinematics.