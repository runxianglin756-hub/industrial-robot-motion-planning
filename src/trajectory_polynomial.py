import numpy as np
import matplotlib.pyplot as plt


def quintic_trajectory(q0, qf, T, steps):

    time = np.linspace(
        0,
        T,
        steps
    )


    a0 = q0

    a1 = 0

    a2 = 0


    a3 = (
        10 * (qf - q0)
        /
        T**3
    )


    a4 = (
        -15 * (qf - q0)
        /
        T**4
    )


    a5 = (
        6 * (qf - q0)
        /
        T**5
    )


    position = (
        a0
        +
        a1*time
        +
        a2*time**2
        +
        a3*time**3
        +
        a4*time**4
        +
        a5*time**5
    )


    velocity = (
        a1
        +
        2*a2*time
        +
        3*a3*time**2
        +
        4*a4*time**3
        +
        5*a5*time**4
    )


    acceleration = (
        2*a2
        +
        6*a3*time
        +
        12*a4*time**2
        +
        20*a5*time**3
    )


    return (
        time,
        position,
        velocity,
        acceleration
    )



if __name__ == "__main__":


    q0 = 0

    qf = 90

    T = 5

    steps = 100


    t, q, dq, ddq = quintic_trajectory(
        q0,
        qf,
        T,
        steps
    )


    plt.figure(figsize=(8,5))

    plt.plot(
        t,
        q
    )

    plt.xlabel("Time (s)")
    plt.ylabel("Position (deg)")
    plt.title("Quintic Position Profile")
    plt.grid()

    plt.savefig(
        "../results/quintic_position.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()



    plt.figure(figsize=(8,5))

    plt.plot(
        t,
        dq
    )

    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (deg/s)")
    plt.title("Quintic Velocity Profile")
    plt.grid()

    plt.savefig(
        "../results/quintic_velocity.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()



    plt.figure(figsize=(8,5))

    plt.plot(
        t,
        ddq
    )

    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (deg/s²)")
    plt.title("Quintic Acceleration Profile")
    plt.grid()

    plt.savefig(
        "../results/quintic_acceleration.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


    print("Quintic trajectory completed")