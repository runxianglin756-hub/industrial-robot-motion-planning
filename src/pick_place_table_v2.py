import pybullet as p
import pybullet_data
import time
import math


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


# =========================
# Camera
# =========================

p.resetDebugVisualizerCamera(
    cameraDistance=1.6,
    cameraYaw=45,
    cameraPitch=-35,
    cameraTargetPosition=[
        0.45,
        0,
        0.8
    ]
)



# =========================
# Environment
# =========================

p.loadURDF(
    "plane.urdf"
)


# bigger table

table = p.loadURDF(
    "table/table.urdf",
    [
        0.55,
        0,
        0
    ],
    globalScaling=1.8
)



# =========================
# Panda
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
        0.55,
        0,
        0.72
    ],
    globalScaling=2
)



# =========================
# Move arm
# =========================

def move_arm(pos):

    quat = p.getQuaternionFromEuler(
        [
            math.pi,
            0,
            0
        ]
    )


    joints = p.calculateInverseKinematics(
        robot,
        ik_link,
        pos,
        quat,
        restPoses=[
            0,
            -0.6,
            0,
            -2.2,
            0,
            1.6,
            0
        ]
    )


    for i in range(7):

        p.setJointMotorControl2(
            robot,
            i,
            p.POSITION_CONTROL,
            joints[i],
            force=500,
            maxVelocity=3
        )


    for _ in range(100):

        p.stepSimulation()

        time.sleep(1/500)



# =========================
# Home pose
# =========================

def move_home():

    home = [
        0,
        -0.5,
        0,
        -2.0,
        0,
        1.5,
        0
    ]


    for i in range(7):

        p.setJointMotorControl2(
            robot,
            i,
            p.POSITION_CONTROL,
            home[i],
            force=500,
            maxVelocity=3
        )


    for _ in range(150):

        p.stepSimulation()

        time.sleep(1/500)



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


    for _ in range(50):

        p.stepSimulation()

        time.sleep(1/500)



# =========================
# Attach
# =========================

def attach_cube():

    cid = p.createConstraint(
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
        maxForce=200
    )


    return cid



# =========================
# Pick Place
# =========================


print("Open")

open_gripper()



# Move above cube

print("Above cube")

move_arm(
    [
        0.55,
        0,
        1.0
    ]
)



# Lower

print("Lower")

move_arm(
    [
        0.55,
        0,
        0.74
    ]
)



time.sleep(0.5)



# Close

print("Close")

close_gripper()



time.sleep(1)



# Attach

constraint = attach_cube()

print("Attached")



# Lift

print("Lift")

move_arm(
    [
        0.55,
        0,
        1.05
    ]
)



# Move to center of table

print("Move place")

move_arm(
    [
        0.45,
        0.25,
        1.0
    ]
)



# Lower place

print("Place")

move_arm(
    [
        0.45,
        0.25,
        0.78
    ]
)



time.sleep(1)



# Release

print("Release")


p.removeConstraint(
    constraint
)



open_gripper()



time.sleep(1)



# move away

move_arm(
    [
        0.45,
        0.25,
        1.0
    ]
)



# home

print("Home")

move_home()



print("Finished")



while True:

    p.stepSimulation()

    time.sleep(1/500)