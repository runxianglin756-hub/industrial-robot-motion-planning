import pybullet as p
import pybullet_data
import time
import math
import os
import csv
import matplotlib.pyplot as plt

physicsClient = p.connect(p.GUI)

if physicsClient < 0:
    raise Exception("Failed to connect to PyBullet")

p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.resetSimulation()
p.setGravity(0, 0, -9.81)

os.makedirs("results", exist_ok=True)

p.loadURDF("plane.urdf")

robot_id = p.loadURDF(
    "kuka_iiwa/model.urdf",
    basePosition=[0, 0, 0],
    useFixedBase=True
)

num_joints = p.getNumJoints(robot_id)
ee_index = num_joints - 1

print("Robot joints:", num_joints)

steps = 400
radius = 0.25
center = [0.5, 0, 0.5]

ideal_x = []
ideal_y = []
ideal_z = []

real_x = []
real_y = []
real_z = []

try:
    for i in range(steps):

        t = 2 * math.pi * i / steps

        x = center[0] + radius * math.cos(t)
        y = center[1] + radius * math.sin(t)
        z = center[2]

        ideal_x.append(x)
        ideal_y.append(y)
        ideal_z.append(z)

        joint_positions = p.calculateInverseKinematics(
            robot_id,
            ee_index,
            [x, y, z]
        )

        for j in range(num_joints):
            p.setJointMotorControl2(
                robot_id,
                j,
                p.POSITION_CONTROL,
                joint_positions[j],
                force=300
            )

        p.stepSimulation()

        state = p.getLinkState(robot_id, ee_index)
        pos = state[0]

        real_x.append(pos[0])
        real_y.append(pos[1])
        real_z.append(pos[2])

        time.sleep(1 / 240)

except Exception as e:
    print(e)

error = []

for i in range(len(real_x)):
    e = math.sqrt(
        (ideal_x[i] - real_x[i]) ** 2 +
        (ideal_y[i] - real_y[i]) ** 2 +
        (ideal_z[i] - real_z[i]) ** 2
    )
    error.append(e)

with open("results/trajectory_data.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "real_x",
        "real_y",
        "real_z",
        "ideal_x",
        "ideal_y",
        "ideal_z",
        "error"
    ])

    for i in range(len(real_x)):
        writer.writerow([
            real_x[i],
            real_y[i],
            real_z[i],
            ideal_x[i],
            ideal_y[i],
            ideal_z[i],
            error[i]
        ])

plt.figure()
plt.plot(ideal_x, ideal_y, label="Ideal Trajectory")
plt.plot(real_x, real_y, label="Actual Trajectory")
plt.axis("equal")
plt.xlabel("X")
plt.ylabel("Y")
plt.title("End Effector Trajectory")
plt.legend()
plt.grid()
plt.savefig("results/trajectory.png", dpi=300)
plt.close()

plt.figure()
plt.plot(error)
plt.xlabel("Step")
plt.ylabel("Error (m)")
plt.title("Trajectory Tracking Error")
plt.grid()
plt.savefig("results/error.png", dpi=300)
plt.close()

rmse = math.sqrt(
    sum([e ** 2 for e in error]) / len(error)
)

print("RMSE:", rmse)
print("Results saved in results folder")

if p.isConnected():
    p.disconnect()