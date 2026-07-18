import pybullet as p
import pybullet_data
import time
import math


p.connect(p.GUI)

p.setAdditionalSearchPath(
    pybullet_data.getDataPath()
)


robot=p.loadURDF(
    "franka_panda/panda.urdf",
    useFixedBase=True
)


ee=8


target=[
0.45,
0,
0.45
]


quat=p.getQuaternionFromEuler(
[
math.pi,
0,
0
]
)


joint=p.calculateInverseKinematics(

    robot,

    ee,

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



while True:


    for i in range(7):

        p.setJointMotorControl2(

            robot,

            i,

            p.POSITION_CONTROL,

            joint[i],

            force=100

        )


    p.stepSimulation()

    time.sleep(1/240)