import pybullet as p
import pybullet_data
import time


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


table_shape = p.createCollisionShape(
    p.GEOM_BOX,
    halfExtents=[
        0.5,
        0.5,
        0.05
    ]
)


table_visual = p.createVisualShape(
    p.GEOM_BOX,
    halfExtents=[
        0.5,
        0.5,
        0.05
    ]
)


table = p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=table_shape,
    baseVisualShapeIndex=table_visual,
    basePosition=[
        0,
        0,
        0.05
    ]
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


print("Environment created")


while True:

    p.stepSimulation()

    time.sleep(
        1/240
    )