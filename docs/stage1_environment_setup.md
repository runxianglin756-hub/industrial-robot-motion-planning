Stage 1: Development Environment Setup

1. Stage Goal

The goal of Stage 1 is to set up the robot simulation environment and make sure PyBullet can run correctly.

In this stage, I mainly needed to:

- Install the required software
- Set up the Python environment
- Install PyBullet
- Open the PyBullet simulation window
- Load a ground plane
- Load a robot arm model
- Print robot joint information
- Control the robot joints and make the robot move


2. Software Used

The software and tools I used were:

- VS Code: used to write and run Python code
- Miniforge / Conda: used to manage the Python environment
- Python 3.10: used as the programming language
- PyBullet: used for robot simulation
- NumPy: used for numerical computation
- Matplotlib: used for plotting later
- SciPy: used for scientific computing later


3. Project Folder Structure

The project folder is organized like this:

ur5_robot_project/
- docs/
- models/
- results/
- src/
  - main.py

Explanation:

docs: stores notes and project documents
models: stores robot model files
results: stores screenshots and test results
src: stores Python code


4. Conda Environment Setup

I created a conda environment named ur5.

The commands were:

conda create -n ur5 python=3.10 -y
conda activate ur5

After activation, the terminal shows:

(ur5)

This means the project is running inside the correct Python environment.


5. Package Installation

I installed PyBullet and other useful Python packages.

The commands were:

conda install -c conda-forge pybullet -y
pip install numpy matplotlib scipy

PyBullet is the most important package in this stage because it is used to run the robot simulation.


6. PyBullet Test

To check whether PyBullet was installed correctly, I used this command:

python -c "import pybullet as p; print('OK')"

The output showed:

OK

This means PyBullet was installed successfully.


7. VS Code Setup

I also configured VS Code to use the correct Python environment.

The correct Python interpreter is from the conda environment ur5.

The path is:

/Users/lin/miniforge3/envs/ur5/bin/python

This step is important because VS Code must use the same environment where PyBullet is installed.


8. First Simulation Test

I wrote a basic Python program in:

src/main.py

The program does these things:

- Opens the PyBullet GUI
- Loads the ground plane
- Loads a robot arm model
- Prints the robot joint names
- Controls the robot joints
- Makes the robot arm move


9. Robot Model Used

In this stage, I used the built-in KUKA iiwa robot model from PyBullet.

This model was used first because it is stable and easy to load.

The robot model path used in the code was:

kuka_iiwa/model.urdf

Later, I will try to replace it with the UR5 robot model.


10. Running the Program

The program can be run with:

conda activate ur5
python src/main.py

If I am already inside the src folder, I can run:

python main.py


11. Result

The simulation ran successfully.

I was able to:

- Open the PyBullet GUI
- Load the ground plane
- Load the robot arm
- Print the joint information
- Make the robot arm move

The robot arm moved in the simulation window, which means the basic environment setup was successful.


12. Problems and Solutions

Problem 1:
PyBullet could not be installed correctly with pip at first.

Solution:
I used Miniforge and conda instead.

Command:

conda install -c conda-forge pybullet -y


Problem 2:
VS Code used the wrong Python interpreter.

Solution:
I changed the VS Code interpreter to:

/Users/lin/miniforge3/envs/ur5/bin/python


Problem 3:
The code used p.sin(), but PyBullet does not have a sin function.

Solution:
I imported the math module and used:

math.sin()


13. Stage 1 Completion Status

Completed:

- Installed VS Code
- Installed Miniforge / Conda
- Created the ur5 Python environment
- Installed PyBullet
- Opened the PyBullet GUI
- Loaded the ground plane
- Loaded a robot arm model
- Printed joint information
- Controlled robot joints
- Made the robot arm move

Not completed yet:

- Import the real UR5 robot model
- Continue learning forward kinematics and inverse kinematics


14. Stage 1 Summary

In Stage 1, I successfully set up the Python and PyBullet simulation environment.

I created a conda environment, installed PyBullet, configured VS Code, and ran a basic robot simulation.

The robot arm could move in the PyBullet GUI, which shows that the environment is working correctly.

The next step is to import the UR5 robot model and continue learning robot kinematics.