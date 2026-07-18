"""
Stage 4 Final Demo

Integrated Pick and Place System

Robot:
Franka Panda 7-DOF

Functions:
- PyBullet simulation
- IK motion control
- Quintic trajectory
- Obstacle avoidance
- Pick and place task

"""


import pybullet as p
import pybullet_data
import time
import math
import numpy as np
import os



# =============================
# Connect
# =============================

p.connect(p.GUI)

p.setAdditionalSearchPath(
    pybullet_data.getDataPath()
)


p.setGravity(
    0,
0,
-10
)


p.configureDebugVisualizer(
    p.COV_ENABLE_GUI,
    0
)



p.resetDebugVisualizerCamera(

    cameraDistance=1.8,

    cameraYaw=30,

    cameraPitch=-35,

    cameraTargetPosition=[
        0.5,
        0.2,
        0.5
    ]

)



# =============================
# Environment
# =============================


p.loadURDF(
    "plane.urdf"
)



table = p.loadURDF(
    "table/table.urdf",
    [
        0.5,
        0,
        0
    ]
)



# obstacle

obstacle_shape = p.createVisualShape(

    p.GEOM_BOX,

    halfExtents=[
        0.12,
        0.12,
        0.15
    ],

    rgbaColor=[
        1,
        0,
        0,
        2
    ]
)



p.createMultiBody(

    baseMass=0,

    baseVisualShapeIndex=
    obstacle_shape,

    basePosition=[
        0.5,
        0.25,
        0.72
    ]
)



# =============================
# Robot
# =============================


robot = p.loadURDF(

    "franka_panda/panda.urdf",

    [
        0,
        -0.35,
        0.65
    ],

    useFixedBase=True

)



arm_joints = range(7)


ik_link = 11


hand_link = 8



# =============================
# Object
# =============================


cube = p.loadURDF(

    "cube_small.urdf",

    [
        0.75,
        -0.25,
        0.68
    ],

    globalScaling=1.5

)



# =============================
# Quintic Motion
# =============================


def quintic(
        q0,
        qf,
        steps=80):


    result=[]


    for i in range(steps):


        s=i/(steps-1)


        h=(
            10*s**3
            -
            15*s**4
            +
            6*s**5
        )


        result.append(
            q0+(qf-q0)*h
        )


    return result




def move_joint(target):


    current=[]


    for j in arm_joints:

        current.append(
            p.getJointState(
                robot,
                j
            )[0]
        )



    trajectory=quintic(

        np.array(current),

        np.array(target[:7])

    )



    for q in trajectory:


        for j in arm_joints:


            p.setJointMotorControl2(

                robot,

                j,

                p.POSITION_CONTROL,

                q[j],

                force=500

            )


        p.stepSimulation()

        time.sleep(0.02)





# =============================
# IK Motion
# =============================


def move_arm(position):


    quat=p.getQuaternionFromEuler(

        [
            math.pi,
            0,
            0
        ]

    )



    joint=p.calculateInverseKinematics(

        robot,

        ik_link,

        position,

        quat

    )


    move_joint(
        joint
    )





# =============================
# Gripper
# =============================


def gripper(open=True):


    value=0.035 if open else 0.005



    p.setJointMotorControl2(

        robot,

        9,

        p.POSITION_CONTROL,

        value,

        force=50

    )


    p.setJointMotorControl2(

        robot,

        10,

        p.POSITION_CONTROL,

        value,

        force=50

    )



    for i in range(30):

        p.stepSimulation()

        time.sleep(0.01)





# =============================
# Attach Object
# =============================


def attach():

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




# =============================
# Draw Labels
# =============================


def markers():


    p.addUserDebugText(

        "PICK",

        [
            0.85,
            -0.25,
            0.8
        ],

        textColorRGB=[
            1,
            1,
            0
        ]

    )



    p.addUserDebugText(

        "PLACE",

        [
            0.15,
            0.35,
            0.8
        ],

        textColorRGB=[
            0,
            1,
            0
        ]

    )

    p.addUserDebugText(

        "obstacle",

        [
            0.55,
            0.2,
            0.9
        ],

        textColorRGB=[
            0,
            0,
            9
        ]

    )



markers()



# =============================
# Task
# =============================


print("Move above cube")


move_arm(

    [
        0.75,
        -0.25,
        0.95
    ]

)



print("Pick")


move_arm(

    [
        0.75,
        -0.25,
        0.73
    ]

)



gripper(False)


time.sleep(1)


constraint=attach()



print("Lift")


move_arm(

    [
        0.75,
        0,
        1.05
    ]

)



print("Avoid obstacle and move")


move_arm(

    [
        0.1,
        0.25,
        1.05
    ]

)



print("Place")


move_arm(

    [
        0.1,
        0.25,
        0.85
    ]

)



time.sleep(1)



print("Release")


p.removeConstraint(
    constraint
)


gripper(True)



print("Return home")


move_arm(

    [
        0,
        0.5,
        1.5
    ]

)



print("DONE")



# keep window

while True:

    p.stepSimulation()

    time.sleep(0.01)