import numpy as np
import matplotlib.pyplot as plt


class CartesianLinearPlanner:
    """
    Cartesian straight line interpolation planner

    Generates intermediate points between
    start and goal positions.
    """


    def __init__(self, start, goal, steps=100):

        self.start = np.array(start)
        self.goal = np.array(goal)
        self.steps = steps



    def generate(self):

        trajectory = []

        for i in range(self.steps + 1):

            ratio = i / self.steps

            point = (
                (1 - ratio) * self.start
                +
                ratio * self.goal
            )

            trajectory.append(point)


        return np.array(trajectory)



if __name__ == "__main__":


    start_position = [
        0.2,
        0.2,
        0.5
    ]


    goal_position = [
        0.8,
        0.6,
        0.4
    ]


    planner = CartesianLinearPlanner(
        start_position,
        goal_position,
        steps=100
    )


    path = planner.generate()



    print("Generated points:")
    print(path)



    # Visualization

    fig = plt.figure(figsize=(8,6))

    ax = fig.add_subplot(
        111,
        projection="3d"
    )


    ax.plot(
        path[:,0],
        path[:,1],
        path[:,2],
        linewidth=3,
        label="Cartesian Linear Path"
    )


    ax.scatter(
        start_position[0],
        start_position[1],
        start_position[2],
        s=80,
        label="Start"
    )


    ax.scatter(
        goal_position[0],
        goal_position[1],
        goal_position[2],
        s=80,
        label="Goal"
    )


    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")


    ax.set_title(
        "Cartesian Linear Interpolation"
    )


    ax.legend()

    plt.show()