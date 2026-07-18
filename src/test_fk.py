from forward_kinematics import forward_kinematics


theta = [
    0,
    -90,
    0,
    -90,
    0,
    0
]


T = forward_kinematics(theta)


print(T)


position = T[:3,3]


print("End Effector Position:")
print(position)