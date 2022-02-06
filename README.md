# 2D Random Walk

## Introduction

This repository contains code for a *2D Random Walk* with the intent of give an answer to the following puzzle.

The full puzzle solution is a requirement to apply to a quantitative position in [Optiver](https://www.optiver.com/working-at-optiver/career-opportunities/). 
For example, see the [Quantitative Researcher](https://www.optiver.com/working-at-optiver/career-opportunities/5841549002/) position for more information.

## Puzzle

### Problem

An ant leaves its anthill in order to forage for food. It moves with the speed of 10cm per second, but it doesn't know where to go, therefore every second it moves randomly 10cm directly north, south, east or west with equal probability.

1) If the food is located on east-west lines 20cm to the north and 20cm to the south, as well as on north-south lines 20cm to the east and 20cm to the west from the anthill, how long will it take the ant to reach it on average?
2) What is the average time the ant will reach food if it is located only on a diagonal line passing through (10cm, 0cm) and (0cm, 10cm) points?
3) Can you write a program that comes up with an estimate of average time to find food for any closed boundary around the anthill? What would be the answer if food is located outside an defined by ( (x – 2.5cm) / 30cm )2 + ( (y – 2.5cm) / 40cm )2 < 1  in coordinate system where the anthill is located at (x = 0cm, y = 0cm)? Provide us with a solution rounded to the nearest integer.

### Solution

My solution to the puzzle is summarized in the [solution](https://github.com/prenassipaolo/optiver_puzzle/blob/main/solution.pdf) file.

In particular, the results I found are:
1) 4.5
2) +∞
3) 14

## Code

### Dependencies

The code is compatible with Python 3. The following dependencies are needed to run the simulation:

* NumPy
* Pandas
* Matplotlib
* seaborn
* copy
* PyYAML


### Highlevel overview of the files

In the top-level directory are executable scripts to execute, evaluate, and
visualize the simulation. The main entry point is in `main.py`.
This file runs the simulation printing the useful metrics on the terminal and dysplaying the ants positions into an external window.

Main tracking code:

* `main.py`: Main function that runs the whole simulation and saves the results.
* `ants.py`: Ants class. It manages the ants positions, performs the steps, calculates the metrics, plots the ants history.
* `constraints.py`: Constraints class. It stores the constraints functions, finds the constraints boundaries and evaluates the points in the euclidian space as inside, outside or boundary points. 
* `grid.py`: Grid class. It populates the grid to dysplay with the ants positions per each time step. 
* `boundary_func.py`: Set of possible boundary functions.
* `utils.py`: Auxiliary functions to evaluate the points, calculate distances and read the configuration file.
* `config.yaml`: Configuration file.


### Installation

First, clone the repository:
```
git clone https://github.com/prenassipaolo/optiver_puzzle.git
```
Then, change the [configuration](https://github.com/prenassipaolo/optiver_puzzle/blob/main/config.yaml) file according to preferred settings.


## Simulation

### Running the simulation

The following example starts the simulation:
```
python main.py 
```

It assumes the available resources are compatible to the configuration parameters. A large sample of ants, a large number of steps or large boundaries could result in errors related to time or available space.


### Generating results

Beside the main tracking application, the scripts could print the exact solution, print the useful metrics and save them into the ```output/histoy.csv```.


The following image shows the final step (according to the default configurations) of a simulation.

![example_final_step](https://github.com/prenassipaolo/optiver_puzzle/blob/main/output/example_final_step.PNG)


**NOTE**: The implemented modules are extremely generic. They could be easily adapted to simulate many different tasks related to a 2D Random Walk.




