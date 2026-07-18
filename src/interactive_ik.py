import pybullet as p
import pybullet_data
import time


# ==========================
# Connect PyBullet
# ==========================

physicsClient = p.connect(p.GUI)

if physicsClient < 0:
    raise Exception("PyBullet connection failed")


p.setAdditionalSearchPath(
    pybullet_data.getDataPath()
)


p.setGravity(
    0,
    0,
    -9.81
)



# ==========================
# Environment
# ==========================

p.loadURDF(
    "plane.urdf"
)



# ==========================
# Load Franka Panda
# ==========================

robot = p.loadURDF(
    "franka_panda/panda.urdf",
    useFixedBase=True
)


print("===================")
print("Robot ID:", robot)
print("===================")



# ==========================
# Robot information
# ==========================

num_joints = p.getNumJoints(robot)

print(
    "Joint number:",
    num_joints
)


for i in range(num_joints):

    info = p.getJointInfo(
        robot,
        i
    )

    print(
        i,
        info[1].decode()
    )



# End effector

ee_link = 11


print(
    "End effector:",
    p.getJointInfo(robot,ee_link)[1].decode()
)



# ==========================
# Disable default motors
# ==========================

for i in range(num_joints):

    p.setJointMotorControl2(

        robot,

        i,

        p.VELOCITY_CONTROL,

        force=0

    )



# ==========================
# Target Cartesian pose
# ==========================

target_position = [

    0.45,   # X

    0.00,   # Y

    0.65    # Z

]


target_orientation = p.getQuaternionFromEuler(

    [

        0,

        -1.57,

        0

    ]

)



print("===================")
print("Target position:")
print(target_position)
print("===================")



# ==========================
# Inverse Kinematics
# ==========================


joint_solution = p.calculateInverseKinematics(

    robot,

    ee_link,

    target_position,

    targetOrientation=target_orientation,


    lowerLimits=[

        -2.8,

        -1.7,

        -2.8,

        -3.0,

        -2.8,

        -0.1,

        -2.8

    ],


    upperLimits=[

        2.8,

        1.7,

        2.8,

        -0.1,

        2.8,

        3.7,

        2.8

    ],


    jointRanges=[

        5.6,

        3.4,

        5.6,

        2.9,

        5.6,

        3.8,

        5.6

    ],


    restPoses=[

        0,

        -0.5,

        0,

        -1.5,

        0,

        1.0,

        0

    ]

)



print("===================")
print("IK solution:")
print("===================")


for i,j in enumerate(joint_solution):

    print(
        i,
        j
    )



# ==========================
# Move robot
# ==========================

arm_joints = [

    0,

    1,

    2,

    3,

    4,

    5,

    6

]



print("===================")
print("Moving robot...")
print("===================")



for step in range(1500):


    if not p.isConnected():

        break



    for i,joint in enumerate(arm_joints):


        p.setJointMotorControl2(

            robot,

            joint,

            p.POSITION_CONTROL,

            targetPosition=joint_solution[i],

            force=300,

            positionGain=0.05,

            velocityGain=1

        )



    p.stepSimulation()


    time.sleep(
        1/240
    )



print("===================")
print("Reached target")
print("===================")



# ==========================
# Print final pose
# ==========================


state = p.getLinkState(

    robot,

    ee_link

)


print(
    "Actual end effector position:"
)

print(
    state[4]
)



# ==========================
# Keep GUI
# ==========================

while p.isConnected():

    p.stepSimulation()

    time.sleep(
        1/240
    )