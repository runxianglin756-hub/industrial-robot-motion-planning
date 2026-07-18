import pybullet as p
import pybullet_data
import time


# =========================
# Connect
# =========================

physicsClient = p.connect(p.GUI)

p.setAdditionalSearchPath(
    pybullet_data.getDataPath()
)

p.setGravity(
    0,0,-9.81
)



# =========================
# Environment
# =========================

plane = p.loadURDF(
    "plane.urdf"
)



# =========================
# Load Panda Robot
# =========================


robot = p.loadURDF(

    "franka_panda/panda.urdf",

    [0,0,0],

    useFixedBase=True

)


print(
    "Robot joints:",
    p.getNumJoints(robot)
)



# Arm joints

arm_joints = [
    0,1,2,3,4,5,6
]


# end effector

ee_link = 11



# =========================
# Cube
# =========================


cube_start = [

    0.55,

    0,

    0.05

]


cube = p.loadURDF(

    "cube_small.urdf",

    cube_start

)



# =========================
# IK function
# =========================


def move_arm(target):


    quat = p.getQuaternionFromEuler(

        [
            0,
            -1.57,
            0
        ]

    )


    joint_positions = p.calculateInverseKinematics(

        robot,

        ee_link,

        target,

        quat,

        lowerLimits=[

            -2.9,
            -1.7,
            -2.9,
            -3.0,
            -2.9,
            -0.1,
            -2.9

        ],

        upperLimits=[

            2.9,
            1.7,
            2.9,
            0,
            2.9,
            3.7,
            2.9

        ],

        jointRanges=[

            5.8,
            3.4,
            5.8,
            3,
            5.8,
            3.8,
            5.8

        ],

        restPoses=[

            0,
            -0.5,
            0,
            -2,
            0,
            1.5,
            0

        ]

    )


    for step in range(300):

        for i,j in enumerate(arm_joints):

            p.setJointMotorControl2(

                robot,

                j,

                p.POSITION_CONTROL,

                joint_positions[i],

                force=100

            )


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

        force=20

    )


    p.setJointMotorControl2(

        robot,

        10,

        p.POSITION_CONTROL,

        0.04,

        force=20

    )




def close_gripper():


    p.setJointMotorControl2(

        robot,

        9,

        p.POSITION_CONTROL,

        0,

        force=50

    )


    p.setJointMotorControl2(

        robot,

        10,

        p.POSITION_CONTROL,

        0,

        force=50

    )





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

        [0,0,0]

    )


    return cid




# =========================
# Main process
# =========================


print("Open gripper")

open_gripper()

time.sleep(1)



print("Move above cube")


move_arm(

    [
        0.55,
        0,
        0.35
    ]

)



print("Move down")


move_arm(

    [
        0.55,
        0,
        0.12
    ]

)


time.sleep(1)



print("Close gripper")

close_gripper()


time.sleep(1)



print("Attach cube")


constraint = attach_cube()



time.sleep(1)



print("Lift")


move_arm(

    [
        0.55,
        0,
        0.45
    ]

)



print("Move to place position")


move_arm(

    [
        0.35,
        0.35,
        0.35
    ]

)



print("Release")


p.removeConstraint(
    constraint
)


open_gripper()



move_arm(

    [
        0.35,
        0.35,
        0.15
    ]

)



print("Pick and Place Finished")



# keep window

while True:

    p.stepSimulation()

    time.sleep(1/240)