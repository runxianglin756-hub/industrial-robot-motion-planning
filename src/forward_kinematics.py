import numpy as np
from dh_matrix import dh_matrix


def forward_kinematics(theta):

    d = [
        0.089,
        0,
        0,
        0.109,
        0.094,
        0.082
    ]

    a = [
        0,
        -0.425,
        -0.392,
        0,
        0,
        0
    ]

    alpha = [
        90,
        0,
        0,
        90,
        -90,
        0
    ]


    T = np.eye(4)


    for i in range(6):

        Ti = dh_matrix(
            theta[i],
            d[i],
            a[i],
            alpha[i]
        )

        T = T @ Ti


    return T