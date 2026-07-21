import numpy as np


class APFCartesianPlanner:
    """
    Cartesian space path planner
    with Artificial Potential Field obstacle avoidance
    """


    def __init__(
            self,
            start,
            goal,
            obstacle,
            step_size=0.05,
            max_iter=150):


        self.start = np.array(start,dtype=float)

        self.goal = np.array(goal,dtype=float)

        self.obstacle = np.array(obstacle,dtype=float)

        self.step_size = step_size

        self.max_iter = max_iter



    def generate(self):

        path=[]


        current=self.start.copy()


        for i in range(self.max_iter):


            path.append(
                current.copy()
            )


            # -----------------
            # Attractive force
            # -----------------

            attractive = (
                self.goal-current
            )


            distance=np.linalg.norm(
                attractive
            )


            if distance < self.step_size:

                break



            attractive /= np.linalg.norm(
                attractive
            )



            # -----------------
            # Repulsive force
            # -----------------

            diff = current-self.obstacle


            obs_distance=np.linalg.norm(
                diff
            )


            repulsive=np.zeros(3)



            influence_distance=0.4



            if obs_distance < influence_distance:


                repulsive = (

                    diff /

                    (obs_distance**3+1e-6)

                )



            # Combine forces

            direction=(

                attractive

                +

                0.08*repulsive

            )



            direction /= np.linalg.norm(
                direction
            )



            current += (

                self.step_size *

                direction

            )



        path.append(
            self.goal.copy()
        )


        return np.array(path)