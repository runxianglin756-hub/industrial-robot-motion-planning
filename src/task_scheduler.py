"""
Stage 4 - Task Scheduler

Industrial Pick and Place Task Sequencing

Sequence:
HOME
MOVE TO PICK
GRASP
MOVE TO PLACE
RELEASE
RETURN HOME

"""


import time
import numpy as np



class TaskScheduler:


    def __init__(self, robot_system):

        self.robot = robot_system


        self.state = "IDLE"



    # ==============================
    # State change
    # ==============================

    def change_state(self, new_state):

        self.state = new_state

        print(
            "[STATE]",
            self.state
        )

        time.sleep(0.8)



    # ==============================
    # Robot Actions
    # ==============================


    def move_home(self):

        self.change_state(
            "MOVE TO HOME"
        )

        print(
            "Robot moving to home position..."
        )



    def move_to_pick(self, pick):

        self.change_state(
            "MOVE TO PICK POINT"
        )

        print(
            "Moving to pick position:",
            pick
        )



    def grasp(self):

        self.change_state(
            "GRASP OBJECT"
        )

        print(
            "Gripper closed. Object attached."
        )



    def move_to_place(self, place):

        self.change_state(
            "MOVE TO PLACE POINT"
        )

        print(
            "Moving to place position:",
            place
        )



    def release(self):

        self.change_state(
            "RELEASE OBJECT"
        )

        print(
            "Gripper opened. Object released."
        )



    def return_home(self):

        self.change_state(
            "RETURN HOME"
        )

        print(
            "Returning to home position..."
        )



    # ==============================
    # Full Task
    # ==============================


    def execute_pick_place_task(
            self,
            pick,
            place):


        print()
        print("==========================")
        print("Starting Pick and Place Task")
        print("==========================")
        print()



        # Generate trajectory

        trajectory = (
            self.robot.generate_pick_place_path(
                pick,
                place
            )
        )


        print(
            "Generated trajectory points:",
            len(trajectory)
        )



        # Execute sequence


        self.move_home()



        self.move_to_pick(
            pick
        )


        self.grasp()



        self.move_to_place(
            place
        )


        self.release()



        self.return_home()



        self.change_state(
            "TASK COMPLETE"
        )



        print()

        print(
            "Pick and place task finished successfully!"
        )



        return trajectory






# =====================================
# Test
# =====================================


if __name__ == "__main__":


    from robot_system import RobotSystem



    robot = RobotSystem()



    scheduler = TaskScheduler(
        robot
    )



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



    trajectory = (
        scheduler.execute_pick_place_task(
            pick,
            place
        )
    )



    robot.plot_path(
        trajectory,
        pick,
        place
    )