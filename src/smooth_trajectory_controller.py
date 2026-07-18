import os
import csv
import time
import numpy as np
import pybullet as p
import pybullet_data

from trajectory_polynomial import quintic_trajectory


base_dir = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(
    base_dir,
    "smooth_trajectory_data.csv"
)


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


end_effector = joint_num - 1


print(
    "Joint number:",
    joint_num
)


start = np.array(
    [
        0.35,
        0.0,
        0.55
    ]
)


end = np.array(
    [
        0.55,
        0.25,
        0.55
    ]
)


T = 5

steps = 100


tx, x, vx, ax = quintic_trajectory(
    start[0],
    end[0],
    T,
    steps
)


ty, y, vy, ay = quintic_trajectory(
    start[1],
    end[1],
    T,
    steps
)


tz, z, vz, az = quintic_trajectory(
    start[2],
    end[2],
    T,
    steps
)



trajectory_data = []



for i in range(steps):


    target = [

        x[i],
        y[i],
        z[i]

    ]


    joint_target = p.calculateInverseKinematics(
        robot_id,
        end_effector,
        target
    )


    for j in range(joint_num):

        p.setJointMotorControl2(
            robot_id,
            j,
            p.POSITION_CONTROL,
            joint_target[j],
            force=500
        )


    for _ in range(60):

        p.stepSimulation()

        time.sleep(
            1/240
        )


    state = p.getLinkState(
        robot_id,
        end_effector
    )


    actual = state[0]


    error = np.linalg.norm(
        np.array(target)
        -
        np.array(actual)
    )


    q = []


    for j in range(joint_num):

        angle = p.getJointState(
            robot_id,
            j
        )[0]

        q.append(
            np.degrees(angle)
        )


    trajectory_data.append(
        [
            i,
            target[0],
            target[1],
            target[2],
            actual[0],
            actual[1],
            actual[2],
            *q,
            error
        ]
    )



header = [

    "step",

    "desired_x",
    "desired_y",
    "desired_z",

    "actual_x",
    "actual_y",
    "actual_z"

]


for i in range(joint_num):

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
        trajectory_data
    )


print(
    "Smooth trajectory saved:"
)

print(
    csv_path
)


time.sleep(3)


p.disconnect()