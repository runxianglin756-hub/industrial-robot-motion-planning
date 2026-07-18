"""
Stage 4 - Robot System Integration

Integrated:
- Cartesian trajectory generation
- Obstacle avoidance
- Pick and place path planning
- Result visualization

Robot:
7-DOF Manipulator

"""


import numpy as np
import matplotlib.pyplot as plt
import os



# =====================================
# Robot System
# =====================================

class RobotSystem:


    def __init__(self):

        print("Robot system initialized")

        self.robot_name = "7-DOF Robot"


        # obstacle position

        self.obstacle = np.array(
            [
                0.5,
                0.5,
                0.3
            ]
        )



    # =====================================
    # Linear interpolation
    # =====================================

    def linear_interpolation(
            self,
            start,
            goal,
            steps=200):


        start = np.array(start)
        goal = np.array(goal)


        trajectory = []


        for i in range(steps):

            ratio = i/(steps-1)


            point = (
                start
                +
                ratio*(goal-start)
            )


            trajectory.append(point)



        return np.array(trajectory)





    # =====================================
    # Obstacle Avoidance
    # =====================================

    def obstacle_avoidance(
            self,
            path):


        new_path = []


        influence_radius = 0.35



        for point in path:


            distance = np.linalg.norm(
                point-self.obstacle
            )


            if distance < influence_radius:


                direction = (
                    point-self.obstacle
                )


                if np.linalg.norm(direction) != 0:


                    direction = (
                        direction /
                        np.linalg.norm(direction)
                    )


                    point = (
                        point
                        +
                        0.15*direction
                    )



            new_path.append(point)



        return np.array(new_path)





    # =====================================
    # Pick and Place Planning
    # =====================================

    def generate_pick_place_path(
            self,
            pick,
            place):


        print("Generating pick and place trajectory...")


        home = np.array(
            [
                0,
                0,
                0.5
            ]
        )



        path_home_pick = self.linear_interpolation(
            home,
            pick,
            200
        )



        path_pick_place = self.linear_interpolation(
            pick,
            place,
            300
        )



        path_place_home = self.linear_interpolation(
            place,
            home,
            200
        )



        path = np.vstack(
            (
                path_home_pick,
                path_pick_place,
                path_place_home
            )
        )



        safe_path = self.obstacle_avoidance(
            path
        )


        return safe_path





    # =====================================
    # Plot and Save
    # =====================================

    def plot_path(
            self,
            path,
            pick,
            place):



        fig = plt.figure(
            figsize=(9,7)
        )


        ax = fig.add_subplot(
            111,
            projection="3d"
        )



        # trajectory

        ax.plot(
            path[:,0],
            path[:,1],
            path[:,2],
            linewidth=3,
            label="Robot Path"
        )



        # home

        ax.scatter(
            0,
            0,
            0.5,
            s=120,
            label="Home"
        )



        # pick

        ax.scatter(
            pick[0],
            pick[1],
            pick[2],
            s=150,
            label="Pick"
        )



        # place

        ax.scatter(
            place[0],
            place[1],
            place[2],
            s=150,
            label="Place"
        )



        # obstacle

        ax.scatter(
            self.obstacle[0],
            self.obstacle[1],
            self.obstacle[2],
            s=180,
            label="Obstacle"
        )



        ax.set_xlabel(
            "X (m)"
        )


        ax.set_ylabel(
            "Y (m)"
        )


        ax.set_zlabel(
            "Z (m)"
        )



        ax.set_title(
            "Stage 4 Integrated Robot Pick and Place Planning"
        )


        ax.legend()



        # =================================
        # Save
        # =================================


        project_path = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )


        result_dir = os.path.join(
            project_path,
            "results"
        )


        os.makedirs(
            result_dir,
            exist_ok=True
        )



        save_path = os.path.join(
            result_dir,
            "stage4_integrated_robot_path.png"
        )



        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )



        print()
        print("==============================")
        print("Figure saved successfully:")
        print(save_path)
        print("==============================")



        plt.show()






# =====================================
# Main Test
# =====================================


if __name__ == "__main__":



    robot = RobotSystem()



    pick = np.array(
        [
            0.25,
            0.25,
            0.35
        ]
    )



    place = np.array(
        [
            0.8,
            0.8,
            0.35
        ]
    )



    trajectory = robot.generate_pick_place_path(
        pick,
        place
    )



    print(
        "Trajectory points:",
        len(trajectory)
    )



    robot.plot_path(
        trajectory,
        pick,
        place
    )