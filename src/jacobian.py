import numpy as np
from forward_kinematics import forward_kinematics


def calculate_jacobian(q):

    q = np.array(q, dtype=float)

    n = len(q)

    J = np.zeros((3, n))

    delta = 0.0001

    current = forward_kinematics(q)

    current_position = current[:3,3]


    for i in range(n):

        q_new = q.copy()

        q_new[i] += delta


        new_T = forward_kinematics(q_new)

        new_position = new_T[:3,3]


        J[:,i] = (
            new_position - current_position
        ) / delta


    return J