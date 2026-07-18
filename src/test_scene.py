import pybullet as p
import pybullet_data
import time


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
    cameraDistance=1.8,
    cameraYaw=45,
    cameraPitch=-35,
    cameraTargetPosition=[
        0.4,
        0,
        0.8
    ]
)


# =========================
# Ground
# =========================

p.loadURDF(
    "plane.urdf"
)



# =========================
# Table
# =========================

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
# Add coordinate axis
# =========================

p.addUserDebugLine(
    [0,0,0.65],
    [0,0,1.0],
    [1,0,0],
    2
)



print("Scene loaded")


# =========================
# Keep running
# =========================

while True:

    p.stepSimulation()

    time.sleep(1/240)