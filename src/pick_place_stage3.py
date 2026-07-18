import pybullet as p
import pybullet_data
import time
import math


# =========================
# connect
# =========================

p.connect(p.GUI)

p.setAdditionalSearchPath(
    pybullet_data.getDataPath()
)

p.setGravity(
    0,0,-9.81
)


# camera
p.resetDebugVisualizerCamera(
    cameraDistance=1.2,
    cameraYaw=50,
    cameraPitch=-35,
    cameraTargetPosition=[0,0,0.3]
)


# =========================
# environment
# =========================

p.loadURDF(
    "plane.urdf"
)


# =========================
# Panda
# =========================

robot=p.loadURDF(
    "franka_panda/panda.urdf",
    useFixedBase=True
)


arm_joints=[
    0,1,2,3,4,5,6
]


ee_link=8



# =========================
# cube
# =========================

cube=p.loadURDF(

    "cube_small.urdf",

    [
        0.45,
        0,
        0.03
    ]

)


# =========================
# IK move
# =========================

def move_arm(target):


    quat=p.getQuaternionFromEuler(

        [
            math.pi,
            0,
            0
        ]

    )


    joints=p.calculateInverseKinematics(

        robot,

        ee_link,

        target,

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


    for t in range(400):


        for i,j in enumerate(arm_joints):


            p.setJointMotorControl2(

                robot,

                j,

                p.POSITION_CONTROL,

                joints[i],

                force=150

            )


        p.stepSimulation()

        time.sleep(1/240)




# =========================
# gripper
# =========================


def open_gripper():


    p.setJointMotorControl2(
        robot,
        9,
        p.POSITION_CONTROL,
        0.04,
        force=40
    )


    p.setJointMotorControl2(
        robot,
        10,
        p.POSITION_CONTROL,
        0.04,
        force=40
    )



def close_gripper():


    p.setJointMotorControl2(
        robot,
        9,
        p.POSITION_CONTROL,
        0,
        force=40
    )


    p.setJointMotorControl2(
        robot,
        10,
        p.POSITION_CONTROL,
        0,
        force=40
    )



# =========================
# attach
# =========================

def attach_object():


    cid=p.createConstraint(

        robot,

        ee_link,

        cube,

        -1,

        p.JOINT_FIXED,

        [0,0,0],

        [0,0,0]

    )


    return cid




# =========================
# task
# =========================


print("Open gripper")

open_gripper()

time.sleep(1)



print("Move above cube")

move_arm(

[
0.45,
0,
0.55
]

)



print("Lower")

move_arm(

[
0.45,
0,
0.18
]

)



time.sleep(1)



print("Close")

close_gripper()

time.sleep(1)



print("Attach cube")

constraint=attach_object()


time.sleep(1)



print("Lift")

move_arm(

[
0.45,
0,
0.55
]

)



print("Move place")

move_arm(

[
0.25,
0.35,
0.55
]

)



print("Release")


p.removeConstraint(
    constraint
)


open_gripper()



move_arm(

[
0.25,
0.35,
0.2
]

)



print("Finished")



while True:

    p.stepSimulation()

    time.sleep(1/240)