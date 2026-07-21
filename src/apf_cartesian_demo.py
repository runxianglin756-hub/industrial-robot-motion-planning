import matplotlib.pyplot as plt
from apf_cartesian_planner import APFCartesianPlanner


start=[
    0.75,
    -0.25,
    1.0
]


goal=[
    0.15,
    0.35,
    1.0
]


obstacle=[
    0.5,
    0.25,
    1.0
]



planner=APFCartesianPlanner(

    start,

    goal,

    obstacle

)



path=planner.generate()



print(
    "Path points:",
    len(path)
)



fig=plt.figure(figsize=(8,6))


ax=fig.add_subplot(
    111,
    projection="3d"
)



ax.plot(

    path[:,0],

    path[:,1],

    path[:,2],

    linewidth=3,

    label="APF Cartesian Path"

)



ax.scatter(

    obstacle[0],

    obstacle[1],

    obstacle[2],

    s=200,

    label="Obstacle"

)



ax.scatter(

    start[0],

    start[1],

    start[2],

    s=80,

    label="Start"

)



ax.scatter(

    goal[0],

    goal[1],

    goal[2],

    s=80,

    label="Goal"

)



ax.set_xlabel("X")

ax.set_ylabel("Y")

ax.set_zlabel("Z")


ax.legend()


plt.title(
    "APF Cartesian Obstacle Avoidance"
)


plt.show()