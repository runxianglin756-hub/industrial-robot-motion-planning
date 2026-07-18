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


# ==========================
# Parameters
# ==========================

q_start = 0.0
q_end = 1.5

T = 4.0

v_max = 0.6       # maximum velocity rad/s
a_max = 1.0       # maximum acceleration rad/s^2


time = np.linspace(
    0,
    T,
    400
)


distance = q_end - q_start


# acceleration time

t_acc = v_max / a_max


# distance during acceleration

d_acc = 0.5 * a_max * t_acc**2


# check if trapezoidal or triangular

if 2*d_acc > distance:

    # triangular profile

    t_acc = np.sqrt(
        distance / a_max
    )

    t_flat = 0

    v_peak = a_max*t_acc

else:

    # trapezoidal profile

    t_flat = (
        distance - 2*d_acc
    ) / v_max

    v_peak = v_max



t1 = t_acc

t2 = t_acc + t_flat

t3 = T



# ==========================
# Generate trajectory
# ==========================

q = []
v = []
a = []


for t in time:


    if t <= t1:

        # acceleration

        acc = a_max

        vel = a_max*t

        pos = (
            q_start
            +0.5*a_max*t**2
        )


    elif t <= t2:

        # constant velocity

        acc = 0

        vel = v_peak

        pos = (
            q_start
            +d_acc
            +v_peak*(t-t1)
        )


    else:

        # deceleration

        td = t-t2

        acc = -a_max

        vel = (
            v_peak
            -a_max*td
        )

        pos = (
            q_end
            -0.5*a_max*(t3-t)**2
        )


    q.append(pos)
    v.append(vel)
    a.append(acc)



q=np.array(q)
v=np.array(v)
a=np.array(a)



# ==========================
# Position
# ==========================

plt.figure(
    figsize=(8,5)
)


plt.plot(
    time,
    q
)


plt.xlabel(
    "Time (s)"
)

plt.ylabel(
    "Position (rad)"
)


plt.title(
    "Trapezoidal Velocity Position Profile"
)


plt.grid()


plt.savefig(
    os.path.join(
        result_dir,
        "trapezoidal_position.png"
    ),
    dpi=300
)


plt.close()



# ==========================
# Velocity
# ==========================

plt.figure(
    figsize=(8,5)
)


plt.plot(
    time,
    v
)


plt.xlabel(
    "Time (s)"
)

plt.ylabel(
    "Velocity (rad/s)"
)


plt.title(
    "Trapezoidal Velocity Profile"
)


plt.grid()


plt.savefig(
    os.path.join(
        result_dir,
        "trapezoidal_velocity.png"
    ),
    dpi=300
)


plt.close()



# ==========================
# Acceleration
# ==========================

plt.figure(
    figsize=(8,5)
)


plt.plot(
    time,
    a
)


plt.xlabel(
    "Time (s)"
)

plt.ylabel(
    "Acceleration (rad/s²)"
)


plt.title(
    "Trapezoidal Acceleration Profile"
)


plt.grid()


plt.savefig(
    os.path.join(
        result_dir,
        "trapezoidal_acceleration.png"
    ),
    dpi=300
)


plt.close()



print("Trapezoidal profile finished")

print(
    "Saved in:",
    result_dir
)