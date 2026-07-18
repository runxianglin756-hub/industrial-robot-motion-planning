import pybullet as p
import pybullet_data
import time
import numpy as np

from numerical_ik import numerical_ik


p.connect(p.GUI)

p.setAdditionalSearchPath(
    pybullet_data.getDataPath()
)

p.resetSimulation()

p.setGravity(
    0,
    0,
    -9.81
)


p.loadURDF(
    "plane.urdf"
)


robot_id = p.loadURDF(
    "kuka_iiwa/model.urdf",
    useFixedBase=True
)


joint_num = p.getNumJoints(robot_id)

print("Joint number:", joint_num)


target = np.array(
    [
        0.4,
        0.2,
        0.5
    ]
)


initial_q = [
    0,
    -90,
    0,
    -90,
    0,
    0
]


joint_angles = numerical_ik(
    target,
    initial_q
)


print("\nIK result:")
print(joint_angles)



for i in range(6):

    p.setJointMotorControl2(
        bodyIndex=robot_id,
        jointIndex=i,
        controlMode=p.POSITION_CONTROL,
        targetPosition=np.radians(joint_angles[i]),
        force=300
    )


for i in range(300):

    p.stepSimulation()

    time.sleep(
        1/240
    )


end_effector_index = joint_num - 1


state = p.getLinkState(
    robot_id,
    end_effector_index
)


actual_position = np.array(
    state[0]
)


print("\nTarget position:")
print(target)


print("\nActual position:")
print(actual_position)


error = np.linalg.norm(
    target - actual_position
)


print("\nPosition error:")
print(error)


while True:

    p.stepSimulation()

    time.sleep(
        1/240
    )