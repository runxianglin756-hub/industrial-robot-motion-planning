import pybullet as p
import pybullet_data
import time
import math
import numpy as np
import csv


# =========================
# Record trajectory
# =========================

trajectory_record = []


# =========================
# Connect
# =========================

p.connect(p.GUI)

p.setAdditionalSearchPath(
    pybullet_data.getDataPath()
)

p.setGravity(
    0,
    0,
    -9.81
)


p.resetDebugVisualizerCamera(
    cameraDistance=1.6,
    cameraYaw=45,
    cameraPitch=-35,
    cameraTargetPosition=[
        0.45,
        0,
        0.75
    ]
)



# =========================
# Environment
# =========================

p.loadURDF(
    "plane.urdf"
)


table = p.loadURDF(
    "table/table.urdf",
    [
        0.55,
        0,
        0
    ]
)



# =========================
# Robot
# =========================

robot = p.loadURDF(
    "franka_panda/panda.urdf",
    [
        0,
        0,
        0.65
    ],
    useFixedBase=True
)


ik_link = 11
hand_link = 8



# =========================
# Cube
# =========================

cube = p.loadURDF(
    "cube_small.urdf",
    [
        0.70,
        0,
        0.68
    ],
    globalScaling=1.5
)



# =========================
# Quintic trajectory
# =========================

def quintic_trajectory(
        q0,
        qf,
        steps=60
):

    traj=[]

    for i in range(steps):

        s=i/(steps-1)


        h = (
            10*s**3
            -15*s**4
            +6*s**5
        )


        q = q0 + (qf-q0)*h

        traj.append(q)


    return traj




# =========================
# Smooth joint control
# =========================

def move_joint_smooth(target):


    current=[]


    for i in range(7):

        state=p.getJointState(
            robot,
            i
        )

        current.append(
            state[0]
        )


    current=np.array(current)

    target=np.array(
        target[:7]
    )


    traj=quintic_trajectory(
        current,
        target
    )


    for q in traj:


        trajectory_record.append(
            q.copy()
        )


        for i in range(7):

            p.setJointMotorControl2(
                robot,
                i,
                p.POSITION_CONTROL,
                q[i],
                force=500,
                maxVelocity=3
            )


        p.stepSimulation()

        time.sleep(1/240)




# =========================
# IK move
# =========================

def move_arm(
        pos,
        ori=None
):


    if ori is None:

        ori=[
            math.pi,
            0,
            0
        ]


    quat=p.getQuaternionFromEuler(
        ori
    )


    target=p.calculateInverseKinematics(
        robot,
        ik_link,
        pos,
        quat
    )


    move_joint_smooth(
        target
    )




# =========================
# Gripper
# =========================

def open_gripper():

    p.setJointMotorControl2(
        robot,
        9,
        p.POSITION_CONTROL,
        0.035,
        force=50
    )


    p.setJointMotorControl2(
        robot,
        10,
        p.POSITION_CONTROL,
        0.035,
        force=50
    )


    for _ in range(25):

        p.stepSimulation()

        time.sleep(1/500)




def close_gripper():

    p.setJointMotorControl2(
        robot,
        9,
        p.POSITION_CONTROL,
        0.005,
        force=100
    )


    p.setJointMotorControl2(
        robot,
        10,
        p.POSITION_CONTROL,
        0.005,
        force=100
    )


    for _ in range(30):

        p.stepSimulation()

        time.sleep(1/500)




# =========================
# Attach cube
# =========================

def attach_cube():

    cid=p.createConstraint(
        robot,
        hand_link,
        cube,
        -1,
        p.JOINT_FIXED,
        [0,0,0],
        [0,0,0],
        [0,0,0]
    )


    p.changeConstraint(
        cid,
        maxForce=100
    )


    return cid




# =========================
# Home
# =========================

def home():

    target=[
        0,
        -0.5,
        0,
        -2,
        0,
        1.5,
        0
    ]


    move_joint_smooth(
        target
    )



# =========================
# Pick and Place
# =========================


print("Open")

open_gripper()



print("Above cube")

move_arm(
    [
        0.70,
        0,
        0.95
    ]
)



print("Grab")

move_arm(
    [
        0.70,
        0,
        0.70
    ]
)



close_gripper()


time.sleep(0.3)



constraint=attach_cube()



print("Lift")

move_arm(
    [
        0.70,
        0,
        1.05
    ]
)



print("Rotate")

move_arm(
    [
        0.70,
        0,
        1.05
    ],
    [
        math.pi,
        0,
        math.pi/2
    ]
)



print("Move")

move_arm(
    [
        0.35,
        0.25,
        0.95
    ],
    [
        math.pi,
        0,
        math.pi/2
    ]
)



print("Place")

move_arm(
    [
        0.35,
        0.25,
        0.72
    ],
    [
        math.pi,
        0,
        math.pi/2
    ]
)



time.sleep(0.5)



print("Release")

p.removeConstraint(
    constraint
)


open_gripper()



for _ in range(50):

    p.stepSimulation()

    time.sleep(1/240)



move_arm(
    [
        0.35,
        0.25,
        1.05
    ]
)



print("Home")

home()



# =========================
# Save trajectory CSV
# =========================

import os


trajectory_file = (
    "/Users/lin/Desktop/ur5_robot_project/src/"
    "trajectory_data.csv"
)


# make sure folder exists

os.makedirs(
    os.path.dirname(trajectory_file),
    exist_ok=True
)



with open(
    trajectory_file,
    "w",
    newline=""
) as f:


    writer = csv.writer(f)


    writer.writerow(
        [
            "joint1",
            "joint2",
            "joint3",
            "joint4",
            "joint5",
            "joint6",
            "joint7"
        ]
    )


    writer.writerows(
        trajectory_record
    )



print(
    "Trajectory saved:"
)

print(
    trajectory_file
)



# =========================
# Auto close
# =========================

time.sleep(3)

p.disconnect()

print("Simulation closed")