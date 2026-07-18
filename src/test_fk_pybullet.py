import pybullet as p
import pybullet_data
import numpy as np

from forward_kinematics import forward_kinematics


p.connect(p.GUI)

p.setAdditionalSearchPath(
    pybullet_data.getDataPath()
)

robot_id = p.loadURDF(
    "kuka_iiwa/model.urdf",
    useFixedBase=True
)


num_joints = p.getNumJoints(robot_id)

print("Joint number:", num_joints)


joint_angles = []


for i in range(6):

    state = p.getJointState(
        robot_id,
        i
    )

    joint_angles.append(
        np.degrees(state[0])
    )


print("Joint angles:")
print(joint_angles)


T = forward_kinematics(
    joint_angles
)


fk_position = T[:3,3]


print("FK position:")
print(fk_position)



state = p.getLinkState(
    robot_id,
    6
)


pb_position = np.array(
    state[0]
)


print("PyBullet position:")
print(pb_position)



error = np.linalg.norm(
    fk_position - pb_position
)


print("Position Error:")
print(error)