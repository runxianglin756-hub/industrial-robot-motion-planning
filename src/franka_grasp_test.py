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
# Environment
# =========================

plane = p.loadURDF(
    "plane.urdf"
)


# =========================
# Panda robot
# =========================

robot = p.loadURDF(
    "franka_panda/panda.urdf",
    [0,0,0],
    useFixedBase=True
)


# real hand link
ee_link = 8


# =========================
# Cube
# =========================

cube = p.loadURDF(
    "cube_small.urdf",
    [
        0.55,
        0,
        0.05
    ],
    globalScaling=1
)


# =========================
# Print joints
# =========================

print("Joints:")

for i in range(p.getNumJoints(robot)):

    info = p.getJointInfo(robot,i)

    print(
        i,
        info[1].decode()
    )


# =========================
# IK movement
# =========================

def move_arm(pos, quat):

    joint = p.calculateInverseKinematics(
        robot,
        ee_link,
        pos,
        quat
    )


    for i in range(7):

        p.setJointMotorControl2(
            robot,
            i,
            p.POSITION_CONTROL,
            joint[i],
            force=300,
            positionGain=0.05
        )


    for _ in range(300):

        p.stepSimulation()
        time.sleep(1/240)



# =========================
# Gripper
# =========================


def open_gripper():

    p.setJointMotorControl2(
        robot,
        9,
        p.POSITION_CONTROL,
        0.04,
        force=50
    )

    p.setJointMotorControl2(
        robot,
        10,
        p.POSITION_CONTROL,
        0.04,
        force=50
    )


    for _ in range(120):
        p.stepSimulation()
        time.sleep(1/240)



def close_gripper():

    p.setJointMotorControl2(
        robot,
        9,
        p.POSITION_CONTROL,
        0,
        force=80
    )


    p.setJointMotorControl2(
        robot,
        10,
        p.POSITION_CONTROL,
        0,
        force=80
    )


    for _ in range(150):

        p.stepSimulation()
        time.sleep(1/240)



# =========================
# Attach cube
# =========================


def attach_cube():

    cid = p.createConstraint(
        robot,
        ee_link,
        cube,
        -1,
        p.JOINT_FIXED,
        [0,0,0],
        [0,0,0],
        [0,0,0]
    )


    print("Cube attached")

    return cid



# =========================
# Main
# =========================


# gripper vertical down

quat = p.getQuaternionFromEuler(
    [
        math.pi,
        0,
        0
    ]
)


print("Open gripper")

open_gripper()



# move above cube

print("Move above cube")

move_arm(
    [
        0.55,
        0,
        0.20
    ],
    quat
)



time.sleep(1)



# move down

print("Move down")

move_arm(
    [
        0.55,
        0,
        0.12
    ],
    quat
)



time.sleep(1)



# close fingers

print("Close")

close_gripper()



time.sleep(2)



# attach

constraint = attach_cube()


time.sleep(2)



# lift

print("Lift")

move_arm(
    [
        0.55,
        0,
        0.35
    ],
    quat
)


print("Finished")



while True:

    p.stepSimulation()

    time.sleep(1/240)