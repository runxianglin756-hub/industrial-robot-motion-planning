import os
import csv
import time
import numpy as np
import pybullet as p
import pybullet_data

from trajectory_planning import linear_trajectory


base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "trajectory_data.csv")


p.connect(p.GUI)

p.setAdditionalSearchPath(pybullet_data.getDataPath())

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

end_effector = joint_num - 1


active_joints = []

for i in range(joint_num):

    joint_type = p.getJointInfo(robot_id, i)[2]

    if joint_type != p.JOINT_FIXED:
        active_joints.append(i)


print("Robot joints:", joint_num)

print("Active joints:", active_joints)



start_point = np.array(
    [
        0.35,
        0.00,
        0.55
    ]
)


end_point = np.array(
    [
        0.55,
        0.25,
        0.55
    ]
)


trajectory = linear_trajectory(
    start_point,
    end_point,
    80
)


initial_q = p.calculateInverseKinematics(
    robot_id,
    end_effector,
    start_point.tolist()
)


for i, joint in enumerate(active_joints):

    p.resetJointState(
        robot_id,
        joint,
        initial_q[i]
    )



data = []


for step, target in enumerate(trajectory):


    if not p.isConnected():

        p.connect(p.GUI)

        p.setAdditionalSearchPath(
            pybullet_data.getDataPath()
        )



    q_target = p.calculateInverseKinematics(
        robot_id,
        end_effector,
        target.tolist()
    )


    for i, joint in enumerate(active_joints):

        p.setJointMotorControl2(
            robot_id,
            joint,
            p.POSITION_CONTROL,
            q_target[i],
            force=500
        )


    for _ in range(80):

        p.stepSimulation()

        time.sleep(
            1 / 240
        )


    state = p.getLinkState(
        robot_id,
        end_effector
    )


    actual = np.array(
        state[0]
    )


    q_actual = []


    for joint in active_joints:

        angle = p.getJointState(
            robot_id,
            joint
        )[0]

        q_actual.append(
            np.degrees(angle)
        )


    error = np.linalg.norm(
        target - actual
    )


    row = [

        step,

        target[0],
        target[1],
        target[2],

        actual[0],
        actual[1],
        actual[2]

    ]


    row.extend(
        q_actual
    )


    row.append(
        error
    )


    data.append(row)



header = [

    "time_step",

    "desired_x",
    "desired_y",
    "desired_z",

    "actual_x",
    "actual_y",
    "actual_z"

]


for i in range(len(active_joints)):

    header.append(
        "q" + str(i+1)
    )


header.append(
    "error"
)



with open(
    csv_path,
    "w",
    newline=""
) as f:


    writer = csv.writer(f)

    writer.writerow(
        header
    )

    writer.writerows(
        data
    )


print()
print("CSV saved:")
print(csv_path)

print(
    "Points:",
    len(data)
)


time.sleep(3)


p.disconnect()