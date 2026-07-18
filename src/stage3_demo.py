import pybullet as p
import pybullet_data
import numpy as np
import time
import os


# ==========================
# Path
# ==========================

project_path = "/Users/lin/Desktop/ur5_robot_project"

result_dir = os.path.join(
    project_path,
    "results"
)

os.makedirs(
    result_dir,
    exist_ok=True
)



# ==========================
# Waypoints
# ==========================

waypoints = np.array([

    [0.0, 0.0],

    [0.15, 0.12],

    [0.25, 0.25],

    [0.35, 0.18],

    [0.50, 0.10],

    [0.65, 0.15],

    [0.80, 0.35],

    [0.90, 0.65],

    [1.00, 1.00]

])



# ==========================
# Smooth interpolation
# ==========================

path = []


for i in range(len(waypoints)-1):

    start = waypoints[i]

    end = waypoints[i+1]


    for s in np.linspace(
        0,
        1,
        10
    ):

        point = (
            (1-s)*start
            +
            s*end
        )

        path.append(point)



path = np.array(path)



print(
    "Trajectory points:",
    len(path)
)



# ==========================
# PyBullet
# ==========================

p.connect(
    p.GUI
)


p.configureDebugVisualizer(
    p.COV_ENABLE_GUI,
    0
)


p.setAdditionalSearchPath(
    pybullet_data.getDataPath()
)


p.setGravity(
    0,
    0,
    -9.8
)



# Camera

p.resetDebugVisualizerCamera(

    cameraDistance=1.5,

    cameraYaw=45,

    cameraPitch=-35,

    cameraTargetPosition=[

        0.5,
        0.5,
        0.15

    ]

)



# ==========================
# Ground
# ==========================

p.loadURDF(
    "plane.urdf"
)



# ==========================
# Table
# ==========================

table_shape = p.createVisualShape(

    p.GEOM_BOX,

    halfExtents=[

        0.8,
        0.8,
        0.05

    ],

    rgbaColor=[

        0.55,
        0.35,
        0.15,
        1

    ]

)


p.createMultiBody(

    baseMass=0,

    baseVisualShapeIndex=table_shape,

    basePosition=[

        0.5,
        0.5,
        -0.05

    ]

)



# ==========================
# Obstacle
# ==========================

obstacle_shape = p.createVisualShape(

    p.GEOM_BOX,

    halfExtents=[

        0.12,
        0.12,
        0.12

    ],

    rgbaColor=[

        1,
        0,
        0,
        1

    ]

)



p.createMultiBody(

    baseMass=0,

    baseVisualShapeIndex=obstacle_shape,

    basePosition=[

        0.5,
        0.5,
        0.12

    ]

)



# ==========================
# Draw path
# ==========================

for i in range(
    0,
    len(path)-1,
    5
):

    p.addUserDebugLine(

        [

            path[i][0],
            path[i][1],
            0.12

        ],

        [

            path[i+1][0],
            path[i+1][1],
            0.12

        ],

        [

            0,
            0,
            1

        ],

        3

    )



# ==========================
# Moving object
# ==========================

object_shape = p.createVisualShape(

    p.GEOM_SPHERE,

    radius=0.06,

    rgbaColor=[

        0,
        1,
        0,
        1

    ]

)



obj = p.createMultiBody(

    baseMass=0,

    baseVisualShapeIndex=object_shape,

    basePosition=[

        path[0][0],
        path[0][1],
        0.12

    ]

)

# ==========================
# Start / Goal markers
# ==========================


# Start marker (blue)

start_marker = p.createVisualShape(

    p.GEOM_CYLINDER,

    radius=0.08,

    length=0.01,

    rgbaColor=[

        0,
        0,
        1,
        1

    ]

)


p.createMultiBody(

    baseMass=0,

    baseVisualShapeIndex=start_marker,

    basePosition=[

        path[0][0],
        path[0][1],
        0.005

    ]

)



# Goal marker (green)

goal_marker = p.createVisualShape(

    p.GEOM_CYLINDER,

    radius=0.08,

    length=0.01,

    rgbaColor=[

        0,
        1,
        0,
        1

    ]

)



p.createMultiBody(

    baseMass=0,

    baseVisualShapeIndex=goal_marker,

    basePosition=[

        path[-1][0],
        path[-1][1],
        0.005

    ]

)



# Text labels

p.addUserDebugText(

    "START",

    [

        path[0][0],
        path[0][1],
        0.03

    ],

    textColorRGB=[

        0,
        0,
        1

    ],

    textSize=1.5

)



p.addUserDebugText(

    "GOAL",

    [

        path[-1][0],
        path[-1][1],
        0.03

    ],

    textColorRGB=[

        0,
        1,
        0

    ],

    textSize=1.5

)



# ==========================
# Motion
# ==========================

print(
    "Motion start"
)



for i in range(len(path)-1):


    start = path[i]

    end = path[i+1]


    for s in np.linspace(

        0,
        1,
        8

    ):


        current = (

            (1-s)*start

            +

            s*end

        )



        p.resetBasePositionAndOrientation(

            obj,

            [

                current[0],
                current[1],
                0.12

            ],

            [

                0,
                0,
                0,
                1

            ]

        )



        p.stepSimulation()


        time.sleep(
            0.05
        )



print(
    "Motion finished"
)



# ==========================
# Keep window
# ==========================

while True:

    p.stepSimulation()

    time.sleep(
        0.01
    )