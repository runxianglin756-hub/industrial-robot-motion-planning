import numpy as np
import matplotlib.pyplot as plt


def linear_trajectory(start, end, steps):

    trajectory = []

    start = np.array(start)
    end = np.array(end)

    for i in range(steps):

        t = i / (steps - 1)

        point = start + t * (end - start)

        trajectory.append(point)

    return np.array(trajectory)



if __name__ == "__main__":


    start = [
        0.35,
        0.00,
        0.55
    ]


    end = [
        0.55,
        0.25,
        0.55
    ]


    steps = 100


    trajectory = linear_trajectory(
        start,
        end,
        steps
    )


    print("Trajectory points:")
    print(trajectory)


    plt.figure(figsize=(7,6))


    plt.plot(
        trajectory[:,0],
        trajectory[:,1],
        marker="."
    )


    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")


    plt.title(
        "Linear Cartesian Trajectory"
    )


    plt.grid()

    plt.axis("equal")


    plt.savefig(
        "../results/linear_trajectory.png",
        dpi=300,
        bbox_inches="tight"
    )


    plt.show()