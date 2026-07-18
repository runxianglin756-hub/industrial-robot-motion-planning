import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
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
# Time
# ==========================

T = 4.0

N = 400

t = np.linspace(
    0,
    T,
    N
)



# ==========================
# Cubic Polynomial
# ==========================

def cubic(q0, qf, T, t):

    a0 = q0

    a1 = 0

    a2 = (
        3*(qf-q0)
        /
        T**2
    )

    a3 = (
        -2*(qf-q0)
        /
        T**3
    )


    q = (
        a0
        +
        a1*t
        +
        a2*t**2
        +
        a3*t**3
    )


    return q



# ==========================
# Quintic Polynomial
# ==========================

def quintic(q0,qf,T,t):


    a0 = q0

    a1 = 0

    a2 = 0


    a3 = (
        10*(qf-q0)
        /
        T**3
    )


    a4 = (
        -15*(qf-q0)
        /
        T**4
    )


    a5 = (
        6*(qf-q0)
        /
        T**5
    )


    q = (

        a0
        +
        a1*t
        +
        a2*t**2
        +
        a3*t**3
        +
        a4*t**4
        +
        a5*t**5

    )


    return q



# ==========================
# Generate trajectory
# ==========================


q0 = 0

qf = 1.5



cubic_path = cubic(
    q0,
    qf,
    T,
    t
)



quintic_path = quintic(
    q0,
    qf,
    T,
    t
)



# ==========================
# Velocity
# ==========================


cubic_vel = np.gradient(
    cubic_path,
    t
)


quintic_vel = np.gradient(
    quintic_path,
    t
)



# ==========================
# Acceleration
# ==========================


cubic_acc = np.gradient(
    cubic_vel,
    t
)


quintic_acc = np.gradient(
    quintic_vel,
    t
)



# ==========================
# Save CSV
# ==========================


data = pd.DataFrame(
    {

        "time":t,

        "cubic_position":cubic_path,

        "quintic_position":quintic_path,

        "cubic_velocity":cubic_vel,

        "quintic_velocity":quintic_vel,

        "cubic_acceleration":cubic_acc,

        "quintic_acceleration":quintic_acc

    }
)



csv_path = os.path.join(
    result_dir,
    "trajectory_comparison.csv"
)



data.to_csv(
    csv_path,
    index=False
)



# ==========================
# Position Plot
# ==========================


plt.figure(
    figsize=(8,5)
)


plt.plot(
    t,
    cubic_path,
    label="Cubic"
)


plt.plot(
    t,
    quintic_path,
    label="Quintic"
)



plt.xlabel(
    "Time (s)"
)


plt.ylabel(
    "Position (rad)"
)


plt.title(
    "Position Comparison"
)


plt.grid()


plt.legend()



plt.savefig(
    os.path.join(
        result_dir,
        "position_comparison.png"
    ),
    dpi=300
)



plt.close()



# ==========================
# Velocity Plot
# ==========================


plt.figure(
    figsize=(8,5)
)


plt.plot(
    t,
    cubic_vel,
    label="Cubic"
)


plt.plot(
    t,
    quintic_vel,
    label="Quintic"
)



plt.xlabel(
    "Time (s)"
)


plt.ylabel(
    "Velocity (rad/s)"
)


plt.title(
    "Velocity Comparison"
)


plt.grid()


plt.legend()



plt.savefig(
    os.path.join(
        result_dir,
        "velocity_comparison.png"
    ),
    dpi=300
)


plt.close()



# ==========================
# Acceleration Plot
# ==========================


plt.figure(
    figsize=(8,5)
)


plt.plot(
    t,
    cubic_acc,
    label="Cubic"
)


plt.plot(
    t,
    quintic_acc,
    label="Quintic"
)



plt.xlabel(
    "Time (s)"
)


plt.ylabel(
    "Acceleration (rad/s²)"
)


plt.title(
    "Acceleration Comparison"
)


plt.grid()


plt.legend()



plt.savefig(
    os.path.join(
        result_dir,
        "acceleration_comparison.png"
    ),
    dpi=300
)



plt.close()



print(
    "Trajectory comparison finished"
)


print(
    "Saved files:"
)


print(
    "position_comparison.png"
)


print(
    "velocity_comparison.png"
)


print(
    "acceleration_comparison.png"
)


print(
    "trajectory_comparison.csv"
)