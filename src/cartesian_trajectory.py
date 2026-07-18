import numpy as np
import matplotlib.pyplot as plt
import os
import pybullet as p
import pybullet_data


# ==========================
# Path
# ==========================

project_path = "/Users/lin/Desktop/ur5_robot_project"


data_file = os.path.join(
    project_path,
    "src",
    "trajectory_data.csv"
)


result_dir = os.path.join(
    project_path,
    "results"
)


os.makedirs(
    result_dir,
    exist_ok=True
)



# ==========================
# Load joint trajectory
# ==========================

joint_data = np.loadtxt(
    data_file,
    delimiter=",",
    skiprows=1
)


print(
    "Trajectory points:",
    len(joint_data)
)



# ==========================
# Start PyBullet
# ==========================

p.connect(
    p.DIRECT
)


p.setAdditionalSearchPath(
    pybullet_data.getDataPath()
)



# ==========================
# Load KUKA iiwa
# ==========================

robot = p.loadURDF(
    "kuka_iiwa/model.urdf",
    useFixedBase=True
)


num_joints = p.getNumJoints(
    robot
)


print(
    "Robot joints:",
    num_joints
)



# ==========================
# Forward Kinematics
# ==========================

ee_positions = []


for q in joint_data:


    # Set 7 joint angles

    for i in range(7):

        p.resetJointState(
            robot,
            i,
            q[i]
        )


    # Get end effector position

    state = p.getLinkState(
        robot,
        num_joints - 1,
        computeForwardKinematics=True
    )


    position = state[4]


    ee_positions.append(
        position
    )



ee_positions = np.array(
    ee_positions
)



p.disconnect()



print(
    "Forward kinematics finished"
)



# ==========================
# Find important points
# ==========================

# Start

start_index = 0


# Pick = lowest end-effector height

pick_index = np.argmin(
    ee_positions[:,2]
)


# Place = final point

place_index = len(ee_positions)-1



print(
    "Start index:",
    start_index
)

print(
    "Pick index:",
    pick_index
)

print(
    "Place index:",
    place_index
)



# ==========================
# Plot Cartesian trajectory
# ==========================

fig = plt.figure(
    figsize=(9,7)
)


ax = fig.add_subplot(
    111,
    projection="3d"
)



# trajectory

ax.plot(
    ee_positions[:,0],
    ee_positions[:,1],
    ee_positions[:,2],
    linewidth=2,
    label="End-effector path"
)



# Start

ax.scatter(
    ee_positions[start_index,0],
    ee_positions[start_index,1],
    ee_positions[start_index,2],
    s=90,
    label="Start"
)



# Pick

ax.scatter(
    ee_positions[pick_index,0],
    ee_positions[pick_index,1],
    ee_positions[pick_index,2],
    s=90,
    label="Pick"
)



# Place

ax.scatter(
    ee_positions[place_index,0],
    ee_positions[place_index,1],
    ee_positions[place_index,2],
    s=90,
    label="Place"
)



# Labels

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
    "7-DOF Robot End-Effector Cartesian Trajectory"
)



ax.legend()


plt.tight_layout()



# ==========================
# Save
# ==========================

save_path = os.path.join(
    result_dir,
    "end_effector_trajectory_3d.png"
)



plt.savefig(
    save_path,
    dpi=300
)



plt.close()



print()

print(
    "Cartesian trajectory saved:"
)

print(
    save_path
)