import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import savgol_filter


# =========================
# Path
# =========================

data_file = (
    "/Users/lin/Desktop/ur5_robot_project/src/"
    "trajectory_data.csv"
)


result_dir = (
    "/Users/lin/Desktop/ur5_robot_project/"
    "results"
)


os.makedirs(
    result_dir,
    exist_ok=True
)



# =========================
# Load CSV
# =========================

data = np.loadtxt(
    data_file,
    delimiter=",",
    skiprows=1
)



print("Original data shape:")
print(data.shape)



# =========================
# Smooth joint trajectory
# =========================

data = savgol_filter(
    data,
    window_length=31,
    polyorder=3,
    axis=0
)



# sampling time

dt = 1/120


time = np.arange(
    len(data)
) * dt



# =========================
# Position
# =========================

plt.figure(
    figsize=(10,5)
)


for i in range(7):

    plt.plot(
        time,
        data[:,i],
        label=f"Joint {i+1}"
    )


plt.xlabel(
    "Time (s)"
)

plt.ylabel(
    "Joint Angle (rad)"
)


plt.title(
    "Joint Position Trajectory"
)


plt.grid()

plt.legend()


plt.tight_layout()


plt.savefig(
    os.path.join(
        result_dir,
        "joint_position.png"
    ),
    dpi=300
)


plt.close()



# =========================
# Velocity
# =========================

velocity = np.gradient(
    data,
    dt,
    axis=0
)


velocity = savgol_filter(
    velocity,
    31,
    3,
    axis=0
)



plt.figure(
    figsize=(10,5)
)


for i in range(7):

    plt.plot(
        time,
        velocity[:,i],
        label=f"Joint {i+1}"
    )


plt.xlabel(
    "Time (s)"
)


plt.ylabel(
    "Velocity (rad/s)"
)


plt.title(
    "Joint Velocity Profile"
)


plt.grid()

plt.legend()


plt.tight_layout()


plt.savefig(
    os.path.join(
        result_dir,
        "joint_velocity.png"
    ),
    dpi=300
)


plt.close()



# =========================
# Acceleration
# =========================

acceleration = np.gradient(
    velocity,
    dt,
    axis=0
)



acceleration = savgol_filter(
    acceleration,
    31,
    3,
    axis=0
)



plt.figure(
    figsize=(10,5)
)



for i in range(7):

    plt.plot(
        time,
        acceleration[:,i],
        label=f"Joint {i+1}"
    )


plt.xlabel(
    "Time (s)"
)


plt.ylabel(
    "Acceleration (rad/s²)"
)


plt.title(
    "Joint Acceleration Profile"
)


plt.grid()

plt.legend()


plt.tight_layout()


plt.savefig(
    os.path.join(
        result_dir,
        "joint_acceleration.png"
    ),
    dpi=300
)


plt.close()



# =========================
# Finish
# =========================

print()
print("Visualization finished")

print(
    "Saved:"
)


print(
    os.path.join(
        result_dir,
        "joint_position.png"
    )
)


print(
    os.path.join(
        result_dir,
        "joint_velocity.png"
    )
)


print(
    os.path.join(
        result_dir,
        "joint_acceleration.png"
    )
)