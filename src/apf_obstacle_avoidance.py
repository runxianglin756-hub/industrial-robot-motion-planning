import numpy as np
import matplotlib.pyplot as plt
import pybullet as p
import pybullet_data
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
# Start / Goal / Obstacle
# ==========================

start = np.array(
    [0.0, 0.0]
)

goal = np.array(
    [1.0, 1.0]
)


obstacle = np.array(
    [0.5, 0.5]
)



# ==========================
# APF Parameters
# ==========================

ka = 1.0        # attractive force

kr = 2.5        # repulsive force

kt = 1.0        # tangential force


d0 = 0.6        # influence distance

step = 0.015

max_iter = 1200



# ==========================
# Attractive Force
# ==========================

def attractive_force(pos):

    return ka * (goal - pos)



# ==========================
# Repulsive Force
# ==========================

def repulsive_force(pos):

    diff = pos - obstacle

    distance = np.linalg.norm(diff)


    if distance >= d0:

        return np.array(
            [0.0, 0.0]
        )


    force = (
        kr
        *
        (
            1 / distance
            -
            1 / d0
        )
        *
        1 / (distance ** 2)
    )


    return (
        force
        *
        diff / distance
    )



# ==========================
# Tangential Force
# ==========================

def tangential_force(pos):

    diff = pos - obstacle

    distance = np.linalg.norm(diff)


    if distance >= d0:

        return np.array(
            [0.0, 0.0]
        )


    tangent = np.array(
        [
            -diff[1],
            diff[0]
        ]
    )


    tangent = (
        tangent
        /
        np.linalg.norm(tangent)
    )


    return kt * tangent



# ==========================
# Generate Path
# ==========================

path = []

current = start.copy()


for i in range(max_iter):


    path.append(
        current.copy()
    )


    F_att = attractive_force(
        current
    )


    F_rep = repulsive_force(
        current
    )


    F_tan = tangential_force(
        current
    )


    F = (
        F_att
        +
        F_rep
        +
        F_tan
    )


    norm = np.linalg.norm(F)


    if norm < 1e-6:

        break


    direction = F / norm


    current = (
        current
        +
        step * direction
    )


    if np.linalg.norm(
        current - goal
    ) < 0.03:


        path.append(
            goal
        )

        break



path = np.array(
    path
)


print(
    "Generated path points:",
    len(path)
)



# ==========================
# Plot
# ==========================

plt.figure(
    figsize=(8,7)
)


plt.plot(
    path[:,0],
    path[:,1],
    linewidth=3,
    label="Modified APF Path"
)


plt.scatter(
    start[0],
    start[1],
    s=120,
    label="Start"
)


plt.scatter(
    goal[0],
    goal[1],
    s=120,
    label="Goal"
)


plt.scatter(
    obstacle[0],
    obstacle[1],
    s=150,
    label="Obstacle"
)



# safety radius

circle = plt.Circle(
    obstacle,
    d0,
    fill=False,
    linewidth=2
)


plt.gca().add_patch(
    circle
)



plt.xlabel(
    "X (m)"
)


plt.ylabel(
    "Y (m)"
)


plt.title(
    "Modified Artificial Potential Field Obstacle Avoidance"
)


plt.axis(
    "equal"
)


plt.grid()


plt.legend(
    loc="upper left"
)



save_path = os.path.join(
    result_dir,
    "apf_path.png"
)


plt.savefig(
    save_path,
    dpi=300,
    bbox_inches="tight"
)


plt.close()



print(
    "Saved:",
    save_path
)



# ==========================
# PyBullet Visualization
# ==========================

p.connect(
    p.GUI
)


p.setAdditionalSearchPath(
    pybullet_data.getDataPath()
)


p.setGravity(
    0,
    0,
    -9.8
)



p.loadURDF(
    "plane.urdf"
)



# obstacle box

obstacle_visual = p.createVisualShape(
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
    baseVisualShapeIndex=obstacle_visual,
    basePosition=[
        obstacle[0],
        obstacle[1],
        0.12
    ]
)



# draw path

for i in range(len(path)-1):

    p.addUserDebugLine(

        [
            path[i][0],
            path[i][1],
            0.05
        ],

        [
            path[i+1][0],
            path[i+1][1],
            0.05
        ],

        [
            0,
            0,
            1
        ],

        4
    )



# moving sphere

sphere = p.createVisualShape(
    p.GEOM_SPHERE,
    radius=0.05,
    rgbaColor=[
        0,
        1,
        0,
        1
    ]
)



robot = p.createMultiBody(
    baseMass=0,
    baseVisualShapeIndex=sphere,
    basePosition=[
        start[0],
        start[1],
        0.05
    ]
)



for point in path:


    p.resetBasePositionAndOrientation(

        robot,

        [
            point[0],
            point[1],
            0.05
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
        0.03
    )



print(
    "APF simulation finished"
)



while True:

    p.stepSimulation()

    time.sleep(
        0.01
    )