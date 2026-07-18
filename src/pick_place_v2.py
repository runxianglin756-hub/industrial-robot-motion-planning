import pybullet as p
import pybullet_data
import time
import math


# connect

p.connect(p.GUI)

p.setAdditionalSearchPath(
    pybullet_data.getDataPath()
)


p.setGravity(
    0,0,-9.8
)



# plane

p.loadURDF(
    "plane.urdf"
)



# robot

robot=p.loadURDF(

    "franka_panda/panda.urdf",

    useFixedBase=True

)


ee_link=11


arm_joints=[
0,1,2,3,4,5,6
]



# cube

cube=p.loadURDF(

    "cube_small.urdf",

    [
    0.45,
    0,
    0.025
    ]

)



# --------------------
# move
# --------------------


def move_arm(pos):


    quat=p.getQuaternionFromEuler(

        [
        0,
        math.pi,
        0
        ]

    )


    joints=p.calculateInverseKinematics(

        robot,

        ee_link,

        pos,

        quat

    )


    for t in range(500):


        for i,j in enumerate(arm_joints):


            p.setJointMotorControl2(

                robot,

                j,

                p.POSITION_CONTROL,

                joints[i],

                force=200,

                positionGain=0.05

            )


        p.stepSimulation()

        time.sleep(1/240)




# --------------------
# gripper
# --------------------


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





# --------------------
# pick place
# --------------------


print("open")

open_gripper()

time.sleep(1)



print("above cube")


move_arm(

[
0.45,
0,
0.25
]

)



print("down")


move_arm(

[
0.45,
0,
0.08
]

)


time.sleep(1)



print("close")


close_gripper()


time.sleep(2)



print("lift")


move_arm(

[
0.45,
0,
0.35
]

)



print("place")


move_arm(

[
0.25,
0.35,
0.35
]

)



print("release")


open_gripper()



while True:

    p.stepSimulation()

    time.sleep(1/240)