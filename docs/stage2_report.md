# Stage 2: Inverse Kinematics and Trajectory Tracking

## 1. Objective

The objective of Stage 2 is to implement inverse kinematics and trajectory tracking for an industrial robot simulation.

The main goals of this stage are:

- Implement inverse kinematics to calculate joint angles from desired end-effector positions.
- Generate Cartesian trajectories between target positions.
- Control robot motion in the PyBullet simulation environment.
- Record and analyze robot tracking performance.


## 2. Inverse Kinematics Implementation

A numerical inverse kinematics method based on the Jacobian pseudo-inverse was implemented.

The joint update equation is:

Δq = J⁺e

where:

- J represents the robot Jacobian matrix.
- J⁺ represents the pseudo-inverse of the Jacobian matrix.
- e represents the position error between the desired and current end-effector position.

The algorithm iteratively updates the joint angles until the end-effector reaches the desired position with a small error.


## 3. Trajectory Planning

A Cartesian linear trajectory was generated for the robot end-effector.

The trajectory was created by interpolating between the initial and target positions.

Initial position:

x = 0.35 m  
y = 0.00 m  
z = 0.55 m


Target position:

x = 0.55 m  
y = 0.25 m  
z = 0.55 m


The trajectory contains 80 intermediate points.

Each Cartesian point is converted into joint commands through inverse kinematics before being executed by the robot controller.


## 4. Robot Control and Data Collection

The calculated joint commands were applied to the robot simulation using PyBullet position control.

During execution, the system recorded:

- Desired end-effector position.
- Actual end-effector position.
- Joint angle values.
- Tracking error.

The recorded trajectory data was saved as:

trajectory_data.csv


The complete control pipeline is:

Trajectory Planning

↓

Inverse Kinematics

↓

Joint Position Control

↓

Robot Motion Simulation

↓

Performance Evaluation


## 5. Results


## 5.1 End-Effector Trajectory

Figure:

results/stage2_trajectory.png


The figure compares the desired trajectory and the actual end-effector trajectory.

The robot successfully follows the planned path. A small deviation appears at the beginning because the robot first moves from its initial configuration to the planned trajectory.


## 5.2 3D End-Effector Trajectory

Figure:

results/stage2_trajectory_3d.png


The 3D trajectory visualization demonstrates that the robot end-effector follows the desired spatial motion path.

The actual trajectory remains close to the desired trajectory, showing successful Cartesian motion control.


## 5.3 Joint Angle Trajectory

Figure:

results/stage2_joint_angles.png


The joint angle trajectory shows the movement of each robot joint during execution.

The joint values change smoothly, indicating stable inverse kinematics solutions and controller performance.


## 5.4 Tracking Error Analysis

Figure:

results/stage2_error.png


The tracking error represents the distance between the desired end-effector position and the actual position.

The maximum tracking error is approximately:

0.025 m


After the initial transient response, the error decreases and remains stable around:

0.02 m


The result demonstrates that the robot controller can achieve stable trajectory tracking.


## 6. Discussion

The Stage 2 implementation successfully demonstrates the complete robot motion pipeline.

The system can:

- Generate desired Cartesian trajectories.
- Solve inverse kinematics problems.
- Convert Cartesian motion into joint commands.
- Execute robot movement in simulation.
- Evaluate tracking accuracy.


The current simulation uses an industrial robot model for validation. The developed framework can be transferred to other six-axis robot models by replacing the robot description file and updating the kinematic parameters.


## 7. Future Improvements

Future improvements include:

- Replace the current robot model with a standard six-axis URDF robot model.
- Implement collision detection and obstacle avoidance.
- Improve trajectory smoothness using velocity and acceleration planning.
- Develop more advanced control methods such as PID or dynamic control.
- Test more complex robot tasks.


## 8. Conclusion

In Stage 2, an inverse kinematics and trajectory tracking system was successfully developed.

The simulation results show that the robot can follow planned Cartesian trajectories with acceptable accuracy.

This stage provides the foundation for future work involving obstacle avoidance, path optimization, and advanced robotic motion planning.