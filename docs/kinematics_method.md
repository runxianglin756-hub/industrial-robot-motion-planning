# Robot Kinematics Method

## Forward Kinematics

The robot forward kinematics is calculated based on Denavit-Hartenberg (DH) parameters.

Each joint transformation is represented by a homogeneous transformation matrix:

A_i = Rot(z,theta_i) Trans(z,d_i) Trans(x,a_i) Rot(x,alpha_i)

The final end-effector pose is obtained by multiplying all joint transformation matrices:

T = A1 A2 ... An


## Inverse Kinematics

The inverse kinematics problem is solved using an iterative numerical method.

The algorithm compares the desired end-effector position with the current position and updates joint angles according to the position error.

The iteration continues until the error reaches the predefined tolerance.


## Verification

The calculated end-effector pose is compared with the PyBullet simulation result to verify the correctness of the kinematic model.