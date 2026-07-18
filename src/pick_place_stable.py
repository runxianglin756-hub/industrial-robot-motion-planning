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
    cameraDistance=1.5,
    cameraYaw=45,
    cameraPitch=-35,
    cameraTargetPosition=[
        0.4,
        0,
        0.9
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
# Panda robot
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



# IK target
ik_link = 11

# hand link
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

def move_arm(position):

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
        position,
        quat
    )


    for i in range(7):

        p.setJointMotorControl2(
            robot,
            i,
            p.POSITION_CONTROL,
            targetPosition=joints[i],
            force=500,
            maxVelocity=3
        )


    for _ in range(100):

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


    for _ in range(50):

        p.stepSimulation()

        time.sleep(1/500)




def close_gripper():

    p.setJointMotorControl2(
        robot,
        9,
        p.POSITION_CONTROL,
        0,
        force=100
    )


    p.setJointMotorControl2(
        robot,
        10,
        p.POSITION_CONTROL,
        0,
        force=100
    )


    for _ in range(50):

        p.stepSimulation()

        time.sleep(1/500)




# =========================
# Attach cube
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


    print("Cube attached")

    return cid




# =========================
# Pick and Place
# =========================


print("Open gripper")

open_gripper()



# -------------------------
# Pick
# -------------------------

print("Move above cube")

move_arm(
    [
        0.55,
        0,
        1.0
    ]
)



print("Lower")

move_arm(
    [
        0.55,
        0,
        0.78
    ]
)



time.sleep(0.5)



print("Close")

close_gripper()


time.sleep(1)



print("Attach")

constraint = attach_cube()


time.sleep(1)



# -------------------------
# Lift
# -------------------------

print("Lift")

move_arm(
    [
        0.55,
        0,
        1.05
    ]
)



# -------------------------
# Move place
# -------------------------

print("Move place")

move_arm(
    [
        0.25,
        0.30,
        1.0
    ]
)



# -------------------------
# Place
# -------------------------

print("Lower to table")

move_arm(
    [
        0.25,
        0.30,
        0.78
    ]
)



time.sleep(1)



# release

print("Release cube")


p.removeConstraint(
    constraint
)



# move away before opening

move_arm(
    [
        0.25,
        0.30,
        0.95
    ]
)



open_gripper()



for _ in range(100):

    p.stepSimulation()

    time.sleep(1/240)



print("Finished")



# =========================
# Keep alive
# =========================

while True:

    p.stepSimulation()

    time.sleep(1/500)