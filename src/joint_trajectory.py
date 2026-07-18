import numpy as np
import matplotlib.pyplot as plt


def quintic_joint_trajectory(
    q_start,
    q_end,
    T,
    steps
):

    time = np.linspace(
        0,
        T,
        steps
    )


    q_start = np.array(
        q_start
    )

    q_end = np.array(
        q_end
    )


    trajectory = []


    for t in time:

        s = t / T


        h = (
            10*s**3
            -
            15*s**4
            +
            6*s**5
        )


        q = (
            q_start
            +
            h *
            (q_end-q_start)
        )


        trajectory.append(q)


    return (
        time,
        np.array(trajectory)
    )



if __name__ == "__main__":


    q_start = [
        0,
        0,
        0,
        0,
        0,
        0
    ]


    q_end = [
        45,
        -30,
        60,
        20,
        90,
        0
    ]


    t, q = quintic_joint_trajectory(
        q_start,
        q_end,
        5,
        100
    )


    plt.figure(
        figsize=(9,6)
    )


    for i in range(6):

        plt.plot(
            t,
            q[:,i],
            label=f"Joint {i+1}"
        )


    plt.xlabel(
        "Time (s)"
    )

    plt.ylabel(
        "Joint Angle (deg)"
    )

    plt.title(
        "Joint Space Trajectory"
    )


    plt.legend()

    plt.grid()


    plt.savefig(
        "../results/joint_space_trajectory.png",
        dpi=300,
        bbox_inches="tight"
    )


    plt.close()


    print(
        "Joint trajectory generated"
    )