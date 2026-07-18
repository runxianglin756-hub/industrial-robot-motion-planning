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


end_effector = joint_num - 1



cube_position = np.array(
    [
        0.4,
        0,
        0.15
    ]
)


grasp_position = [

    cube_position[0],

    cube_position[1],

    cube_position[2] + 0.15

]


print(
    "Target grasp position:",
    grasp_position
)



joint_target = p.calculateInverseKinematics(
    robot,
    end_effector,
    grasp_position
)



for i in range(joint_num):

    p.setJointMotorControl2(
        robot,
        i,
        p.POSITION_CONTROL,
        joint_target[i],
        force=500
    )



for _ in range(1000):

    p.stepSimulation()

    time.sleep(
        1/240
    )


state = p.getLinkState(
    robot,
    end_effector
)


actual_position = state[0]


error = np.linalg.norm(
    np.array(grasp_position)
    -
    np.array(actual_position)
)


print(
    "Actual position:",
    actual_position
)


print(
    "Position error:",
    error
)



while True:

    p.stepSimulation()

    time.sleep(
        1/240
    )