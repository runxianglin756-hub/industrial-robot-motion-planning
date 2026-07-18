import numpy as np
from forward_kinematics import forward_kinematics
from jacobian import calculate_jacobian


def numerical_ik(target, q_initial, max_iterations=200):

    q = np.array(q_initial, dtype=float)

    target = np.array(target, dtype=float)

    learning_rate = 0.5

    tolerance = 0.001

    max_joint_step = 8


    for i in range(max_iterations):

        T = forward_kinematics(q)

        current_position = T[:3, 3]


        error = target - current_position

        error_distance = np.linalg.norm(error)


        print(
            "Iteration:",
            i,
            "Error:",
            error_distance
        )


        if error_distance < tolerance:

            print("IK solved")

            break


        J = calculate_jacobian(q)


        dq = np.linalg.pinv(J) @ error


        dq = np.clip(
            dq,
            -max_joint_step,
            max_joint_step
        )


        q = q + learning_rate * dq


        q = np.clip(
            q,
            -180,
            180
        )


    return q



if __name__ == "__main__":


    target = np.array(
        [
            0.4,
            0.2,
            0.5
        ]
    )


    initial_q = np.array(
        [
            0,
            -90,
            0,
            -90,
            0,
            0
        ]
    )


    result = numerical_ik(
        target,
        initial_q
    )


    print("\nFinal Joint Angles:")
    print(result)


    final_T = forward_kinematics(result)


    final_position = final_T[:3,3]


    print("\nFinal Position:")
    print(final_position)


    final_error = np.linalg.norm(
        target - final_position
    )


    print("\nFinal Error:")
    print(final_error)