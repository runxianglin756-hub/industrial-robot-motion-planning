import numpy as np


def linear_trajectory(start, end, steps):

    trajectory = []

    for i in range(steps):

        t = i/(steps-1)

        point = (
            np.array(start)
            +
            t*(np.array(end)-np.array(start))
        )

        trajectory.append(point)

    return trajectory



if __name__ == "__main__":


    start = [
        0.3,
        0.1,
        0.4
    ]


    end = [
        0.5,
        0.3,
        0.6
    ]


    path = linear_trajectory(
        start,
        end,
        20
    )


    for p in path:
        print(p)