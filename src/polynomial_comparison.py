import numpy as np
import matplotlib.pyplot as plt
import os


# ==========================
# Save path
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

q0 = 0.0        # initial position
qf = 1.5        # final position

v0 = 0.0
vf = 0.0

a0 = 0.0
af = 0.0


T = 4.0

time = np.linspace(
    0,
    T,
    400
)



# ==========================
# Cubic Polynomial
# ==========================

# q(t)=a0+a1t+a2t^2+a3t^3

A = np.array([
    [1,0,0,0],
    [0,1,0,0],
    [1,T,T**2,T**3],
    [0,1,2*T,3*T**2]
])


b = np.array([
    q0,
    v0,
    qf,
    vf
])


cubic_coeff = np.linalg.solve(
    A,
    b
)


a0_c,a1_c,a2_c,a3_c = cubic_coeff



q_cubic = (
    a0_c
    + a1_c*time
    + a2_c*time**2
    + a3_c*time**3
)


v_cubic = (
    a1_c
    + 2*a2_c*time
    + 3*a3_c*time**2
)


acc_cubic = (
    2*a2_c
    + 6*a3_c*time
)



# ==========================
# Quintic Polynomial
# ==========================

# q=a0+a1t+a2t2+a3t3+a4t4+a5t5


A5 = np.array([

    [1,0,0,0,0,0],

    [0,1,0,0,0,0],

    [0,0,2,0,0,0],

    [1,T,T**2,T**3,T**4,T**5],

    [0,1,2*T,3*T**2,4*T**3,5*T**4],

    [0,0,2,6*T,12*T**2,20*T**3]

])


b5 = np.array([

    q0,
    v0,
    a0,
    qf,
    vf,
    af

])


quintic_coeff = np.linalg.solve(
    A5,
    b5
)


a0_q,a1_q,a2_q,a3_q,a4_q,a5_q = quintic_coeff



q_quintic = (
    a0_q
    + a1_q*time
    + a2_q*time**2
    + a3_q*time**3
    + a4_q*time**4
    + a5_q*time**5
)


v_quintic = (
    a1_q
    +2*a2_q*time
    +3*a3_q*time**2
    +4*a4_q*time**3
    +5*a5_q*time**4
)


acc_quintic = (
    2*a2_q
    +6*a3_q*time
    +12*a4_q*time**2
    +20*a5_q*time**3
)



# ==========================
# Plot Position
# ==========================

plt.figure(figsize=(8,5))


plt.plot(
    time,
    q_cubic,
    label="Cubic Polynomial"
)


plt.plot(
    time,
    q_quintic,
    label="Quintic Polynomial"
)


plt.xlabel("Time (s)")
plt.ylabel("Position (rad)")

plt.title(
    "Cubic vs Quintic Polynomial Position"
)


plt.legend()
plt.grid()


plt.savefig(
    os.path.join(
        result_dir,
        "cubic_vs_quintic_position.png"
    ),
    dpi=300
)


plt.close()



# ==========================
# Plot Velocity
# ==========================

plt.figure(figsize=(8,5))


plt.plot(
    time,
    v_cubic,
    label="Cubic Polynomial"
)


plt.plot(
    time,
    v_quintic,
    label="Quintic Polynomial"
)


plt.xlabel("Time (s)")
plt.ylabel("Velocity (rad/s)")


plt.title(
    "Cubic vs Quintic Polynomial Velocity"
)


plt.legend()
plt.grid()


plt.savefig(
    os.path.join(
        result_dir,
        "cubic_vs_quintic_velocity.png"
    ),
    dpi=300
)


plt.close()



# ==========================
# Plot Acceleration
# ==========================

plt.figure(figsize=(8,5))


plt.plot(
    time,
    acc_cubic,
    label="Cubic Polynomial"
)


plt.plot(
    time,
    acc_quintic,
    label="Quintic Polynomial"
)


plt.xlabel("Time (s)")
plt.ylabel("Acceleration (rad/s²)")


plt.title(
    "Cubic vs Quintic Polynomial Acceleration"
)


plt.legend()
plt.grid()


plt.savefig(
    os.path.join(
        result_dir,
        "cubic_vs_quintic_acceleration.png"
    ),
    dpi=300
)


plt.close()



print("Finished")
print("Saved:")
print("cubic_vs_quintic_position.png")
print("cubic_vs_quintic_velocity.png")
print("cubic_vs_quintic_acceleration.png")