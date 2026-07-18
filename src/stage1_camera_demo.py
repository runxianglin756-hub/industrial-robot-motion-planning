import pybullet as p
import pybullet_data
import time
import math

# Connect to PyBullet GUI
p.connect(p.GUI)

# Set environment
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# Load ground plane
p.loadURDF("plane.urdf")

# Load robot model
robot_id = p.loadURDF(
    "kuka_iiwa/model.urdf",
    basePosition=[0, 0, 0],
    useFixedBase=True
)

# Print joint information
num_joints = p.getNumJoints(robot_id)
active_joints = []

print("Number of joints:", num_joints)

for i in range(num_joints):
    joint_info = p.getJointInfo(robot_id, i)
    joint_name = joint_info[1].decode("utf-8")
    joint_type = joint_info[2]

    print(f"Joint {i}: {joint_name}")

    if joint_type == p.JOINT_REVOLUTE:
        active_joints.append(i)

print("Active joints:", active_joints)

# Camera views
camera_views = [
    {
        "name": "Front View",
        "distance": 2.0,
        "yaw": 0,
        "pitch": -30,
        "target": [0, 0, 0.5]
    },
    {
        "name": "Side View",
        "distance": 2.0,
        "yaw": 90,
        "pitch": -30,
        "target": [0, 0, 0.5]
    },
    {
        "name": "Top View",
        "distance": 2.2,
        "yaw": 0,
        "pitch": -89,
        "target": [0, 0, 0.5]
    },
    {
        "name": "Angled View",
        "distance": 2.2,
        "yaw": 45,
        "pitch": -35,
        "target": [0, 0, 0.5]
    }
]

view_index = 0
last_switch_time = time.time()
t = 0.0

while True:
    # Switch camera every 4 seconds
    current_time = time.time()

    if current_time - last_switch_time > 4:
        view_index = (view_index + 1) % len(camera_views)
        view = camera_views[view_index]

        print("Switching camera to:", view["name"])

        p.resetDebugVisualizerCamera(
            cameraDistance=view["distance"],
            cameraYaw=view["yaw"],
            cameraPitch=view["pitch"],
            cameraTargetPosition=view["target"]
        )

        last_switch_time = current_time

    # Move robot joints
    for joint_index in active_joints:
        target = 0.5 * math.sin(t + joint_index)

        p.setJointMotorControl2(
            bodyUniqueId=robot_id,
            jointIndex=joint_index,
            controlMode=p.POSITION_CONTROL,
            targetPosition=target,
            force=200
        )

    p.stepSimulation()
    time.sleep(1 / 240)
    t += 0.01