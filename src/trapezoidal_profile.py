import numpy as np
import matplotlib.pyplot as plt


class TrapezoidalProfile:
    """
    Trapezoidal velocity trajectory generator

    Generates position, velocity and acceleration
    with acceleration, constant velocity and deceleration phases.
    """

    def __init__(self, q0, qf, total_time, vmax, amax):

        self.q0 = q0
        self.qf = qf
        self.T = total_time
        self.vmax = vmax
        self.amax = amax

        self.distance = qf - q0


    def generate(self, dt=0.01):

        t = np.arange(0, self.T + dt, dt)

        distance = abs(self.distance)

        # acceleration time
        ta = self.vmax / self.amax


        # Check if trapezoidal or triangular profile
        if 2 * ta * self.vmax > distance:

            # triangular velocity profile
            ta = np.sqrt(distance / self.amax)
            tv = 0
            vmax = self.amax * ta

        else:

            # normal trapezoidal
            tv = (distance - self.amax * ta**2) / self.vmax
            vmax = self.vmax


        td = ta


        position = []
        velocity = []
        acceleration = []


        direction = np.sign(self.distance)


        for time in t:


            if time < ta:

                # acceleration phase

                acc = self.amax
                vel = acc * time
                pos = 0.5 * acc * time**2


            elif time < ta + tv:

                # constant velocity phase

                acc = 0
                vel = vmax
                pos = (
                    0.5 * self.amax * ta**2
                    + vmax * (time - ta)
                )


            elif time < ta + tv + td:

                # deceleration phase

                tau = time - ta - tv

                acc = -self.amax
                vel = vmax - self.amax * tau

                pos = (
                    0.5 * self.amax * ta**2
                    + vmax * tv
                    + vmax * tau
                    - 0.5 * self.amax * tau**2
                )


            else:

                acc = 0
                vel = 0
                pos = distance


            position.append(self.q0 + direction * pos)

            velocity.append(direction * vel)

            acceleration.append(direction * acc)



        return (
            t,
            np.array(position),
            np.array(velocity),
            np.array(acceleration)
        )



if __name__ == "__main__":


    trajectory = TrapezoidalProfile(
        q0=0,
        qf=1,
        total_time=5,
        vmax=0.4,
        amax=0.5
    )


    t, q, v, a = trajectory.generate()


    plt.figure(figsize=(10,6))


    plt.subplot(3,1,1)
    plt.plot(t,q)
    plt.ylabel("Position")


    plt.subplot(3,1,2)
    plt.plot(t,v)
    plt.ylabel("Velocity")


    plt.subplot(3,1,3)
    plt.plot(t,a)
    plt.ylabel("Acceleration")
    plt.xlabel("Time(s)")


    plt.tight_layout()

    plt.show()