# Ship Routing Optimitzation

## Table of content

* [Introduction](#introduction)
* [Context](#context)
* [Description](#description)
* [Enviroment](#enviroment)
    * [Creation](#creation)
    * [Inputs and Outputs](#inputs-and-outputs)
* [Solutions](#solutions)
* [Conclusions](#conclusions)
* [Final video](#final-video)
* [Author](#author)

## Introduction
This project is the Computer Engineering Final Project. The main motivation was to do a project where I could apply reinforcement learning to solve an IT problem.

## Context
In the sea there are buoys that are specialized in obtaining information from the environment and transfer this information to the ships. In these situations, the problem is that there is no infrastructure to establish communication and it is necessary to use opportunistic protocols to spread the data. In this context, the boats are mobile agents whose location we do not know and the buoys are static elements and we know their location. With opportunistic protocols, communication is available when the mobile agents that want to receive information are close to the static elements that broadcast the data.

## Description
The project wants to solve the previous problem by modifying the route of the boats to cross the maximum number of buoys, but without deviating too much from the destination. To carry out a solution, we first need an environment that simulates the navigation of the boats and their interaction with the buoys and the rest of the elements of the sea and the land.

## Enviroment
The environment is like a game. We have an image of the Atlantic Ocean and we can manage the movement of a ship and we receive a response and a new image with the updated information.

### Creation
<img src="https://github.com/Javier-21/Ship_Routing_Optimitzation/blob/master/rsc/map_enviroment.png" align="right" width="350" alt="Enviroment map"/>

To create the simulator, I used python to code. I took an image of the world and resized the image to have just the Atlantic Ocean as a 100x100 matrix. On the screen there are seven different elements:
* Water: In these cells the ship can move without problems.
* Land: The ship cannot move in these cells.
* Ship: Is the agent that we want to manage.
* Buoys: Are the elements that we want to cross before reaching the destination.
* Storm: They are water cells, but in this case the ship moves slower.
* Ports: There are 5 cells indicating the ports, but only one is the destination port.
* Route line: It is a red line that indicates where the ship was.

### Inputs and Outputs
To simplify the simulator, the ship can only move in 4 directions (north, south, east, west), and this is the only input we need to specify.

The environment output is the updated matrix and a reward. The value of the reward depends on the interaction of the ship with other elements of the map. Possible answers are:
* Interaction with land, without destination port or outside image border: The ship does not move and the environment expects another movement.
* Interaction with water: The reward is -1.
* Interaction with buoy: The reward is 20. If the same buoy is repeated on the same route, the reward is -1.5.
* Interaction with buoy: The reward is -2.
* Interaction with destination port: The reward is 200.
* Interaction with route line: The reward is -1.5.

## Solutions
Now we have the environment to simulate the navigation of the ship. The next step is to implement an algorithm to solve the problem. I have applied a reinforcement learning algorithm. The field is based on learning by trial and error. In order to implement this, we need an environment where we can enter an action, and it returns a reward and a state. This environment is the simulator that I created earlier. The agent that performs the actions and receives the output of the environment is the ship in this project.

<p align="center">
<img src="https://github.com/Javier-21/Ship_Routing_Optimitzation/blob/master/rsc/rl_image.png" width="400" alt="Reinforcement learning"/>
</p>

The specific algorithm I used was Q-learning. To implement this we need to build a matrix with all possible states and for each state all possible moves. For this project we need a 100x100x4 shape matrix. Each cell contains a reward value for performing an action in a specific state. The value is updated using the following formula:

$$ Q^new(s_t, a_t) = (1-$a) $$

One matrix is useful for one destination port, for this reason we need to build five matrix, one for each port. When we have the matrix we must begin to learn, for this we begin to move the ship randomly. During iterations, we started mixing random actions and matrix-based actions. In the end, actions will be taken mostly based on the matrix. To control for chance we need to use a variable ε. This variable will decrease exponentially with the step of the iteration until reaching the minimum.

## Conclusions

## Final video
[![Ship learning](https://img.youtube.com/vi/wj3ZSi1u1rY/0.jpg)](https://www.youtube.com/watch?v=wj3ZSi1u1rY)
<br/>
Click on the image to view the video on YouTube.

## Author
- [Javier Alegre Revuelta](https://github.com/Javier-21)
