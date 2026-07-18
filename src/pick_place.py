import pybullet as p
import pybullet_data
import time
import numpy as np


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


robot = p.loadURDF(
    "kuka_iiwa/model.urdf",
    useFixedBase=True
)


cube_shape = p.createCollisionShape(
    p.GEOM_BOX,
    halfExtents=[
        0.03,
        0.03,
        0.03
    ]
)


cube_visual = p.createVisualShape(
    p.GEOM_BOX,
    halfExtents=[
        0.03,
        0.03,
        0.03
    ]
)


cube = p.createMultiBody(
    baseMass=0.1,
    baseCollisionShapeIndex=cube_shape,
    baseVisualShapeIndex=cube_visual,
    basePosition=[
        0.4,
        0,
        0.15
    ]
)


joint_num = p.getNumJoints(robot)

ee_link = joint_num - 1


cube_position = [
    0.4,
    0,
    0.15
]


pre_grasp = [
    0.4,
    0,
    0.35
]


grasp = [
    0.4,
    0,
    0.20
]


def move_robot(target):

    joint_target = p.calculateInverseKinematics(
        robot,
        ee_link,
        target
    )


    for i in range(joint_num):

        p.setJointMotorControl2(
            robot,
            i,
            p.POSITION_CONTROL,
            joint_target[i],
            force=500
        )


    for _ in range(500):

        p.stepSimulation()

        time.sleep(
            1/240
        )



print("Move to pre-grasp")

move_robot(
    pre_grasp
)


print("Move down")

move_robot(
    grasp
)


print("Gripper close")


constraint = p.createConstraint(
    robot,
    ee_link,
    cube,
    -1,
    p.JOINT_FIXED,
    [0,0,0],
    [0,0,0],
    [0,0,-0.05]
)


time.sleep(1)


print("Lift object")


move_robot(
    pre_grasp
)


print("Place completed")


while True:

    p.stepSimulation()

    time.sleep(
        1/240
    )