import numpy as np
import matplotlib.pyplot as plt


def calculate_velocity(position, dt):

    velocity = np.gradient(
        position,
        dt
    )

    return velocity



def calculate_acceleration(velocity, dt):

    acceleration = np.gradient(
        velocity,
        dt
    )

    return acceleration



if __name__ == "__main__":


    T = 5

    steps = 100


    time = np.linspace(
        0,
        T,
        steps
    )


    q0 = 0

    qf = 90


    q = (
        q0
        +
        (qf-q0)
        *
        (
            10*(time/T)**3
            -
            15*(time/T)**4
            +
            6*(time/T)**5
        )
    )


    dt = time[1]-time[0]


    velocity = calculate_velocity(
        q,
        dt
    )


    acceleration = calculate_acceleration(
        velocity,
        dt
    )


    print(
        "Maximum velocity:",
        np.max(abs(velocity)),
        "deg/s"
    )


    print(
        "Maximum acceleration:",
        np.max(abs(acceleration)),
        "deg/s^2"
    )



    plt.figure(figsize=(8,5))

    plt.plot(
        time,
        q
    )

    plt.xlabel(
        "Time (s)"
    )

    plt.ylabel(
        "Position (deg)"
    )

    plt.title(
        "Joint Position Profile"
    )

    plt.grid()

    plt.savefig(
        "../results/position_profile.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()



    plt.figure(figsize=(8,5))

    plt.plot(
        time,
        velocity
    )

    plt.xlabel(
        "Time (s)"
    )

    plt.ylabel(
        "Velocity (deg/s)"
    )

    plt.title(
        "Joint Velocity Profile"
    )

    plt.grid()

    plt.savefig(
        "../results/velocity_profile.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()



    plt.figure(figsize=(8,5))

    plt.plot(
        time,
        acceleration
    )

    plt.xlabel(
        "Time (s)"
    )

    plt.ylabel(
        "Acceleration (deg/s²)"
    )

    plt.title(
        "Joint Acceleration Profile"
    )

    plt.grid()

    plt.savefig(
        "../results/acceleration_profile.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


    print(
        "Analysis completed"
    )