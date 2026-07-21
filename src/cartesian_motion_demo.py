import pybullet as p
import pybullet_data
import time
import numpy as np


from cartesian_linear_interpolation import CartesianLinearPlanner


# ============================
# Start PyBullet
# ============================

physicsClient = p.connect(
    p.GUI
)

p.setAdditionalSearchPath(
    pybullet_data.getDataPath()
)


p.setGravity(
    0,
    0,
    -9.8
)


# Plane

p.loadURDF(
    "plane.urdf"
)



# ============================
# Load Panda Robot
# ============================

robot = p.loadURDF(
    "franka_panda/panda.urdf",
    useFixedBase=True
)


# ============================
# Robot Parameters
# ============================

end_effector = 11


home_position = [
    0.3,
    0.0,
    0.6
]


target_position = [
    0.6,
    0.4,
    0.45
]



# ============================
# Cartesian Planner
# ============================

planner = CartesianLinearPlanner(
    home_position,
    target_position,
    steps=100
)


trajectory = planner.generate()



print(
    "Generated Cartesian trajectory:",
    len(trajectory)
)



# ============================
# Execute Motion
# ============================

for point in trajectory:


    joint_angles = p.calculateInverseKinematics(
        robot,
        end_effector,
        point
    )


    for joint_id in range(7):

        p.setJointMotorControl2(
            bodyUniqueId=robot,
            jointIndex=joint_id,
            controlMode=p.POSITION_CONTROL,
            targetPosition=joint_angles[joint_id],
            force=200
        )


    p.stepSimulation()


    time.sleep(
        0.05
    )



print(
    "Cartesian linear motion finished"
)



# Keep window open

while True:

    p.stepSimulation()

    time.sleep(0.01)