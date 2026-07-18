import numpy as np
import matplotlib.pyplot as plt
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



# ==================================================
# Cartesian Linear Interpolation
# ==================================================

def linear_interpolation(
        start,
        end,
        points=100):


    trajectory = []


    for s in np.linspace(
        0,
        1,
        points
    ):

        position = (
            (1-s)*start
            +
            s*end
        )

        trajectory.append(
            position
        )


    return np.array(
        trajectory
    )



# ==================================================
# Circular Arc Interpolation
# ==================================================

def circular_interpolation(
        center,
        radius,
        start_angle,
        end_angle,
        points=100):


    trajectory = []


    angles = np.linspace(
        start_angle,
        end_angle,
        points
    )


    for theta in angles:


        x = (
            center[0]
            +
            radius*np.cos(theta)
        )


        y = (
            center[1]
            +
            radius*np.sin(theta)
        )


        z = center[2]


        trajectory.append(
            [
                x,
                y,
                z
            ]
        )


    return np.array(
        trajectory
    )



# ==========================
# Linear Example
# ==========================

start = np.array(
    [
        0.2,
        0.2,
        0.5
    ]
)


end = np.array(
    [
        0.8,
        0.6,
        0.5
    ]
)


linear_path = linear_interpolation(
    start,
    end
)



# ==========================
# Circular Example
# ==========================

center = np.array(
    [
        0.5,
        0.5,
        0.5
    ]
)


radius = 0.3


circle_path = circular_interpolation(
    center,
    radius,
    0,
    np.pi
)



# ==========================
# Plot Linear
# ==========================

fig = plt.figure(
    figsize=(8,6)
)


ax = fig.add_subplot(
    111,
    projection="3d"
)



ax.plot(
    linear_path[:,0],
    linear_path[:,1],
    linear_path[:,2],
    linewidth=3,
    label="Linear Path"
)


ax.scatter(
    start[0],
    start[1],
    start[2],
    s=100,
    label="Start"
)


ax.scatter(
    end[0],
    end[1],
    end[2],
    s=100,
    label="End"
)



ax.set_xlabel(
    "X (m)"
)

ax.set_ylabel(
    "Y (m)"
)

ax.set_zlabel(
    "Z (m)"
)


ax.set_title(
    "Cartesian Linear Interpolation"
)


ax.legend()


plt.savefig(
    os.path.join(
        result_dir,
        "linear_interpolation.png"
    ),
    dpi=300
)


plt.close()



# ==========================
# Plot Circular
# ==========================

fig = plt.figure(
    figsize=(8,6)
)


ax = fig.add_subplot(
    111,
    projection="3d"
)



ax.plot(
    circle_path[:,0],
    circle_path[:,1],
    circle_path[:,2],
    linewidth=3,
    label="Circular Arc"
)



ax.scatter(
    center[0],
    center[1],
    center[2],
    s=100,
    label="Center"
)



ax.set_xlabel(
    "X (m)"
)

ax.set_ylabel(
    "Y (m)"
)

ax.set_zlabel(
    "Z (m)"
)


ax.set_title(
    "Cartesian Circular Arc Interpolation"
)



ax.legend()



plt.savefig(
    os.path.join(
        result_dir,
        "circular_interpolation.png"
    ),
    dpi=300
)


plt.close()



print(
    "Cartesian interpolation finished"
)

print(
    "Saved:"
)

print(
    "linear_interpolation.png"
)

print(
    "circular_interpolation.png"
)